from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from blocks_of_code import CodeBlocks, SUPER_GLOBAL_SCALE_VAR
from astro_database import AstroDatabase
import sys
from importlib.machinery import SourceFileLoader

testing = SourceFileLoader('testing', r"D:\attya-plus\projects\AstroCode\testing.py").load_module()

class OpenProject(QMainWindow):
    def __init__(self):
        # config
        super().__init__()
        self.setWindowTitle("AstroCode - MyProject")
        self.setWindowIcon(QIcon("static/colored_icon.png"))
        self.widget = QWidget()
        self.widget_layout = QHBoxLayout()
        self.widget_layout.setContentsMargins(0,0,0,0)
        self.widget.setLayout(self.widget_layout)
        self.setCentralWidget(self.widget)
        self.setMinimumSize(1550, 770)
        self.setStyleSheet("background-color: #222;")
        # explorer
        self.explorer = QWidget()
        self.explorer_layout = QVBoxLayout()
        self.explorer.setLayout(self.explorer_layout)
        self.explorer.setFixedWidth(280)
        self.explorer_label = QLabel("EXPLORER")
        f = QFont('Arial', 14); f.setBold(True)
        self.explorer_label.setStyleSheet("color: #d0d0d0;")
        self.explorer_label.setAlignment(Qt.AlignCenter)
        self.explorer_label.setFont(f)
        self.explorer_layout.addWidget(self.explorer_label)
        self.explorer_tv = testing.MyWindow()
        self.explorer_tv.setStyleSheet("background-color: #3f3f3f; border-radius: 10px;")
        self.explorer_layout.addWidget(self.explorer_tv)
        self.explorer.setStyleSheet("background-color: #333;")
        self.widget_layout.addWidget(self.explorer)
        # blockspace
        self.blockspace_sa = QScrollArea()
        self.blockspace_sa.setStyleSheet("""
            QWidget {border-width:0px; border-style:solid; border-color:#222; background-color: #2f2f2f;}
            QScrollArea {border-width:0px; border-style:solid; border-color:#222; background-color: #2f2f2f;}
            QScrollBar:vertical {
                border: 0px solid #1e1e1e;
                background-color: #fff;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar:horizontal {
                border: 0px solid #1e1e1e;
                background-color: #fff;
                height: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle {
                background-color: #444;
                min-height: 20px;
            }
            QScrollBar::handle:hover {
                background-color: #4f4f4f;
            }
            QScrollBar::add-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line {
                border: 0px solid #1e1e1e;
                background-color: #1e1e1e;
                height: 0px;
                width: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        self.blockspace_sa.setWidgetResizable(True)
        self.blockspace = QWidget()
        self.blockspace.setFixedSize(QSize(2000, 5000))
        self.blockspace_sa.setWidget(self.blockspace)
        self.blockspace_sa.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.blockspace_sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.widget_layout.addWidget(self.blockspace_sa)
        # blockpicker
        self.blockpicker = QWidget()
        self.blockpicker_layout = QVBoxLayout()
        self.blockpicker.setLayout(self.blockpicker_layout)
        self.blockpicker.setFixedWidth(450)
        self.blockpicker.setStyleSheet("background-color: #333; border-radius: 10px;")
        # self.widget_layout.addWidget(self.blockpicker)
        self.db_viewer = CodeBlocks()
        self.widget_layout.addWidget(self.db_viewer)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(palette)

    window = OpenProject()
    SUPER_GLOBAL_SCALE_VAR['super-main-window'] = window
    
    app.exec_()
