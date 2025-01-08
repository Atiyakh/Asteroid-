from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, sqlite3 as sql

def clear_layout(l:QLayout):
    for i in range(l.count()):
        l.itemAt(i).widget().deleteLater()

class QCustomHeaderView(QHeaderView):
    def resizeEvent(self, _):
        self.filter_sa.setFixedSize(self.width(), self.height() - 36)
        self.filter_sa.move(0, 40)
    def moveEvent(self, _):
        self.filter_sa.setFixedSize(self.width(), self.height() - 36)
        self.filter_sa.move(0, 40)
    def __init__(self, main_, filter_sa):
        self.main_ = main_
        self.filter_sa = filter_sa
        super().__init__(Qt.Orientation.Horizontal)
        self.filter_sa.setParent(self)
        self.setStyleSheet(
            "QHeaderView::section { background-color: #444; color: white; border: 1px solid #666666; padding-left: 10px; margin:2px; margin-bottom: 45px;}"
        )
        self.filter_sa.raise_()
        self.filter_sa.setFixedSize(self.width(), self.height() - 36)
        self.filter_sa.move(0, 40)

class DarkComboBox(QComboBox):
    def wheelEvent(self, _):
        pass

    def getOption(self):
        return self.currentText()

    def setItems(self, items):
        self.clear()
        self.addItems(items)

    def handleIndexChanged(self, _):
        currect_table = self.currentText()
        self.parent.current_table = currect_table
        self.parent.InsertData(currect_table)

    def __init__(self, parent):
        self.parent = parent
        super().__init__(None)
        self.currentIndexChanged.connect(self.handleIndexChanged)
        self.setStyleSheet("""
            QScrollBar:vertical {
                margin: 3px;
                border: 0px solid #1e1e1e;
                background-color: #fff;
                width: 12px;
            }
            QScrollBar:horizontal {
                margin: 3px;
                border: 0px solid #1e1e1e;
                background-color: #fff;
                height: 12px;
            }
            QScrollBar::handle {
                background-color: #444;
            }
            QScrollBar::handle:hover {
                background-color: #4f4f4f;
            }
            QScrollBar::add-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
            }
            QScrollBar::sub-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
            }
            QComboBox {
                outline: 0;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                background-color: #333333;
                color: #ffffff;
                font-size: 16px;
                selection-background-color: #444444;
                selection-color: #ffffff;
            }
            QComboBox::down-arrow {
                image: url("static/down_arrow.png");
            }
            QComboBox::drop-down {
                outline: 0;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #555555;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox QAbstractItemView {
                outline: 0;
                border: 1px solid #555;
                background-color: #333;
                color: #fff;
                font-size: 16px;
                selection-background-color: #444;
                selection-color: #fff;
            }
        """)

class DatabaseView(QWidget):
    def filterTable(self, column, text):
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, column)
            if text.lower() in item.text().lower():
                self.table_widget.setRowHidden(row, False)
            else:
                self.table_widget.setRowHidden(row, True)

    def get_column_names(self, table_name):
        cursor = self.db.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        column_names = [column[1] for column in columns_info]
        self.tables_columns[table_name] = column_names
        return column_names
    
    def get_tables_names(self):
        cur = self.db.cursor()
        cur.execute('SELECT sql, tbl_name FROM "main".sqlite_master WHERE type=?;', ('table',))
        for table_code, table_name in cur.fetchall():
            self.tables_names.append(table_name)
            self.tables_code[table_name] = table_code
        cur.close()
    
    def fetch_data(self, table_name):
        cur = self.db.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        data = cur.fetchall()
        cur.close()
        return data

    def __init__(self, database_path):
        super().__init__()
        self.current_table = None
        self.cells = []
        self.tables_names = []
        self.tables_code = dict()
        self.tables_columns = dict()
        self.db = sql.connect(database_path)
        self.get_tables_names()
        for table_name in self.tables_names:
            self.get_column_names(table_name)
        self.initUI()

    def InsertData(self, table):
        self.cells.clear()
        self.clear_table()
        self.headers = self.tables_columns[table]
        clear_layout(self.filtering_layout)
        for col in range(self.headers.__len__()):
            obj = QLineEdit()
            obj.textChanged.connect(lambda text, col=col: self.filterTable(col, text))
            obj.setFixedHeight(35)
            obj.setMinimumWidth(200)
            obj.setPlaceholderText('filter')
            obj.setStyleSheet("color: #fff; background-color: #111; border-width: 0px; border-radius: 4px; font-family: Arial; font-size: 16px; padding: 2px; margin: 2px;")
            self.filtering_layout.addWidget(obj)
        data = self.fetch_data(table)
        self.table_widget.setColumnCount(len(self.headers))
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        for row, rowData in enumerate(data):
            self.table_widget.insertRow(row)
            row_ = []
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                row_.append(item)
                self.table_widget.setItem(row, col, item)
            self.cells.append(row_)
    
    def RetrieveData(self):
        data_ = []
        col_num = self.headers.__len__()
        for row in range(self.cells.__len__()):
            row_ = [self.cells[row][col].text() for col in range(col_num)]
            data_.append(row_)
        return data_
    
    def clear_table(self):
        self.table_widget.clear()
        self.table_widget.clearSpans()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)

    def initUI(self):
        self.widget_layout = QVBoxLayout(self)
        self.widget_layout.setContentsMargins(5,5,5,5)
        self.widget_layout.setSpacing(2)

        self.table_widget = QTableWidget(self)

        self.upper_widget = QWidget()
        self.upper_widget.setObjectName('uw')
        self.upper_widget.setStyleSheet("#uw { background-color: #333; border: 1px solid #666; border-radius: 10px; }")
        self.upper_layout = QHBoxLayout(self.upper_widget)
        self.upper_layout.setContentsMargins(4,4,4,4)
        self.upper_layout.setSpacing(3)

        self.filtering_widget_sa = QScrollArea(self)
        self.filtering_widget_sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.filtering_widget_sa.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.filtering_widget_sa.setFixedHeight(50)

        self.custom_h_header = QCustomHeaderView(self, self.filtering_widget_sa)
        self.table_widget.setHorizontalHeader(self.custom_h_header)

        def bind_table_widget_h_scroll_to_filters(_):
            self.filtering_widget_sa.horizontalScrollBar().setValue(self.table_widget.horizontalScrollBar().value()*200)
        
        self.table_widget.horizontalScrollBar().valueChanged.connect(bind_table_widget_h_scroll_to_filters)
        self.filtering_widget_sa.wheelEvent = lambda _: None

        self.filtering_widget_sa.setStyleSheet("border-color: #2f2f2f; border-width: 0px; border-style: solid; border-radius: 10px; margin: 0px;")
        self.filtering_widget = QWidget()
        self.filtering_widget_sa.setWidget(self.filtering_widget)
        self.filtering_widget_sa.setWidgetResizable(True)
        self.filtering_widget.setObjectName('uw')
        self.filtering_widget.setStyleSheet("#uw { background-color: #2f2f2f; border-width: 0px; border-radius: 0px; }")
        self.filtering_layout = QHBoxLayout(self.filtering_widget)
        self.filtering_layout.setContentsMargins(0,0,0,0)
        self.filtering_layout.setSpacing(0)

        self.tables_combo = DarkComboBox(self)
        self.tables_combo.addItems(self.tables_names)

        def add_row_button_f(_):
            row_num = self.table_widget.rowCount()
            self.table_widget.insertRow(row_num)
            row_ = []
            for col in range(self.headers.__len__()):
                item = QTableWidgetItem('')
                row_.append(item)
                self.table_widget.setItem(row_num, col, item)
            self.cells.append(row_)
        self.add_row_button = QPushButton()
        self.add_row_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_row_button.clicked.connect(add_row_button_f)
        self.add_row_button.setIcon(QIcon(r"static\plus.png"))
        self.add_row_button.setStyleSheet("background-color: #333; border: 1px solid #666; border-radius: 5px; font-size: 20px; padding: 2px; color: #fff;")
        self.add_row_button.setToolTip('add new row')

        def save_changes_button_f(_):
            cur = self.db.cursor()
            cur.execute(f"DELETE FROM {self.current_table};")
            self.db.commit()
            data = self.RetrieveData()
            len_row = data[0].__len__()
            columns = str(self.headers)[1:-1].replace('"', '').replace("'", '')
            for row_num, row in enumerate(data):
                try:
                    cur.execute(f"INSERT INTO {self.current_table} ({columns}) VALUES({('?,'*len_row)[:-1]});", row)
                except sql.IntegrityError:
                    msg_box = QMessageBox()
                    msg_box.setWindowIcon(self.windowIcon())
                    msg_box.setStyleSheet('''
                        QWidget { background-color:#222; color:#fff; }
                        QPushButton {
                            border-color: #666;
                            border-width: 2px;
                            border-style: solid;
                            border-radius: 5px;
                            padding: 6px;
                        }''')
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText(f"IntegrityError: Data in row {row_num+1} is in a wrong data type.")
                    msg_box.setWindowTitle("Astroid DatabaseViewer Error:")
                    msg_box.addButton("OK", QMessageBox.AcceptRole)
                    msg_box.exec_()
            self.db.commit()
            cur.close()
        self.save_changes_button = QPushButton()
        self.save_changes_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_changes_button.clicked.connect(save_changes_button_f)
        self.save_changes_button.setIcon(QIcon(r"static\save_changes.png"))
        self.save_changes_button.setStyleSheet("background-color: #333; border: 1px solid #666; border-radius: 5px; font-size: 20px; padding: 2px; color: #fff;")
        self.save_changes_button.setToolTip('save changes')

        self.upper_layout.addWidget(self.tables_combo)
        self.upper_layout.addWidget(self.add_row_button)
        self.upper_layout.addWidget(self.save_changes_button)

        self.widget_layout.addWidget(self.upper_widget)
        self.widget_layout.addWidget(self.table_widget)

        self.tables_combo.setFixedHeight(35)
        self.add_row_button.setFixedSize(35, 35)
        self.save_changes_button.setFixedSize(35, 35)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.horizontalHeader().setMinimumSectionSize(200)

        f = QFont("Arial", 10)
        f.setBold(True)

        self.table_widget.verticalHeader().setFont(f)
        self.table_widget.horizontalHeader().setFont(f)

        self.table_widget.verticalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #444; color: white; border: 1px solid #666666; padding-left: 10px; margin:1px; }"
        )

        self.table_widget.setStyleSheet(
            """
            QScrollBar:vertical {
                margin: 3px;
                border: 0px solid #1e1e1e;
                background-color: #fff;
                width: 12px;
            }
            QScrollBar:horizontal {
                margin: 3px;
                border: 0px solid #1e1e1e;
                background-color: #fff;
                height: 12px;
            }
            QScrollBar::handle {
                background-color: #444;
                min-height: 25px;
            }
            QScrollBar::handle:hover {
                background-color: #4f4f4f;
                min-height: 25px;
            }
            QScrollBar::add-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
            }
            QLineEdit {
                background-color: #303030;
                color: white;
                font-family: arial bold;
                font-size: 17px;
                border: 1px solid #303030;
            }
            QScrollBar::sub-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
            }
            QTableView QTableCornerButton::section {
                background-color: #444; 
                border: 1px solid #666666;
                border-radius: 5px;
                margin:1px;
            }
            QTableView {
                padding: 3px;
                background-color: #303030;
                color: white;
                border: 1px solid #505050;
                border-radius: 10px;
                selection-background-color: #3a3a3a;
            }
            QTableView::item:selected:focus {
                border: 1px solid #009ACF
            }
            QTableView::item {
                border-radius: 5px;
                padding: 2px;
                border: 1px solid #505050;
                margin: 1px;
            }
            QTableView::item:selected {
                background-color: #303030;
                color: white;
            }
            QHeaderView {
                border-radius: 5px;
            }
            QHeaderView::section {
                padding: 2px;
                background-color: #505050;
                color: white;
                border: 1px solid #606060;
                border-radius: 5px;
            }
            QTableView {
                outline: 0;
            }
            """
        )
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Astroid Database Viewer - database.sqlite3')
        self.setWindowIcon(QIcon(r"static\colored_icon.png"))

def initiate():
    app = QApplication(sys.argv)
    window = DatabaseView(r"C:\Users\skhodari\Desktop\chinook.db")
    window.show()
    app.exec_()

initiate()
