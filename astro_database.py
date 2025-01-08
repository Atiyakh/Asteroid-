from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from database_table_view import DatabaseView
import sys

class AstroDatabase(QWidget):
    def __init__(self, database_path):
        self.database_path = database_path
        super().__init__()
        self.setWindowTitle(f"Astroied Database Unite:")
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        # left slider
        self.l_slider = QWidget()
        self.l_slider_layout = QVBoxLayout()
        self.l_slider.setLayout(self.l_slider_layout)
        self.l_slider.setStyleSheet("""
            QWidget { background-color: #333; }
            QPushButton {
                background-color: #333;
                color: #fff;
                padding: 7px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444;
                color: #89B4E3;
                padding: 7px;
                border-radius: 5px;
            }
            """)
        self.l_slider.setFixedWidth(260)
        # label
        self.l_slider_label = QLabel("Database Unite")
        f = QFont('Arial', 18)
        self.l_slider_label.setFont(f)
        self.l_slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_slider_label.setStyleSheet("color: #00A2E8; padding-top: 20px; padding-bottom: 20px; border-radius: 5px;")
        self.l_slider_layout.addWidget(self.l_slider_label)
        # buttons
        self.create_tables_button = QPushButton("Update Structure")
        self.create_tables_button.setCursor(Qt.CursorShape.PointingHandCursor)
        f = QFont('Arial', 14); self.create_tables_button.setFont(f)
        self.l_slider_layout.addWidget(self.create_tables_button)

        self.update_structure_button = QPushButton("Set Relationships")
        self.update_structure_button.setCursor(Qt.CursorShape.PointingHandCursor)
        f = QFont('Arial', 14); self.update_structure_button.setFont(f)
        self.l_slider_layout.addWidget(self.update_structure_button)

        self.browse_database_button = QPushButton("Browse Database")
        self.browse_database_button.setCursor(Qt.CursorShape.PointingHandCursor)
        f = QFont('Arial', 14); self.browse_database_button.setFont(f)
        self.l_slider_layout.addWidget(self.browse_database_button)

        self.l_slider_layout.addStretch()
        # main screen
        self.main_screen = QWidget()
        self.main_screen_layout = QVBoxLayout(self.main_screen)
        self.main_screen_layout.setContentsMargins(0,0,0,0)
        self.main_screen.setStyleSheet("background-color: #222;")
        self.main_layout.addWidget(self.main_screen)
        self.main_layout.addWidget(self.l_slider)
        self.main_screen.setMinimumSize(QSize(800, 600))

        db_view = DatabaseView(database_path)
        self.main_screen_layout.addWidget(db_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    update_schema = AstroDatabase(r"C:\Users\skhodari\Desktop\chinook.db")
    update_schema.show()
    app.exec()
