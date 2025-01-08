from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os, pathlib
import time, sqlite3

class WelcomePage(QWidget):
    def project_widget_clicked(self):
        project_button = self.focusWidget()
        project_name = project_button.project_name
        project_description = project_button.project_description
        project_path = project_button.project_path
        date_of_creation = project_button.date_of_creation
        print(project_name, project_description, project_path, date_of_creation)
    def initiate_db(self):
        self.db = sqlite3.connect(os.path.join(pathlib.Path(__file__).parent, 'sqlite3'))
    def seek_projects(self):
        if not hasattr(self, 'db'):
            self.initiate_db()
        cur = self.db.cursor()
        cur.execute("SELECT project_name, project_description, project_path, date_of_creation FROM project;")
        projects = cur.fetchall()
        cur.close()
        return projects
    def insert_into_scroll(self, project_name, project_description, project_path, date_of_creation):
        if 'nothing_to_show' in dir(self): self.nothing_to_show.setParent(None)
        project_widget = QWidget()
        project_widget_layout = QVBoxLayout()
        project_widget.setLayout(project_widget_layout)
        project_widget.setFixedHeight(150)
        project_widget.setStyleSheet('background-color:#444; border-radius:10px; color:#fff')
        project_widget_name = QPushButton(project_name)
        project_widget_name.setCursor(Qt.PointingHandCursor)
        project_widget_name.setStyleSheet("text-align: left;")
        project_widget_name.project_name = project_name
        project_widget_name.project_description = project_description
        project_widget_name.date_of_creation = date_of_creation
        project_widget_name.project_path = project_path
        project_widget_name.clicked.connect(self.project_widget_clicked)
        f = QFont('Arial', 17); f.setBold(True)
        project_widget_name.setFont(f)
        project_widget_layout.addWidget(project_widget_name)
        project_widget_date = QLabel(str(date_of_creation))
        project_widget_layout.addWidget(project_widget_date)
        project_widget_date.setFont(QFont('Arial', 9))
        project_widget_description = QLabel(project_description)
        project_widget_description.setFont(QFont('Arial', 12))
        project_widget_layout.addWidget(project_widget_description)
        self.projects_scrollarea_layout.insertWidget(0, project_widget)
    def __init__(self):
        # config
        super(WelcomePage, self).__init__()
        self.setStyleSheet("background-color: #222;")
        self.widget_layout = QHBoxLayout()
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(QSize(783, 550))
        self.setLayout(self.widget_layout)
        # layout
        self.r_widget = QWidget()
        self.l_widget = QWidget()
        self.l_widget.setFixedWidth(280)
        self.l_widget.setStyleSheet("background-color: #333;")
        self.r_layout = QVBoxLayout()
        self.l_layout = QVBoxLayout()
        self.r_widget.setLayout(self.r_layout)
        self.l_widget.setLayout(self.l_layout)
        for widget in [self.l_widget, self.r_widget]: self.widget_layout.addWidget(widget)
        # create project panel
        self.welcome_label = QLabel(f"Welcome Back!")
        self.welcome_label.setFont(QFont('Helvetica', 18))
        self.welcome_label.setMaximumHeight(50)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color:#fff; background-color: #333; border-radius:10px")
        self.l_layout.addWidget(self.welcome_label)
        self.create_project_form = QWidget()
        self.create_project_form_layout = QVBoxLayout()
        self.create_project_form.setLayout(self.create_project_form_layout)
        self.create_project_form.setStyleSheet("color:#fff; background-color: #444; border-radius:10px")
        self.l_layout.addWidget(self.create_project_form)
        self.create_project_form_label = QLabel("Create Project")
        self.create_project_form_label.setAlignment(Qt.AlignCenter)
        self.create_project_form_label.setFont(QFont('arial', 15))
        self.project_name_label = QLabel('Project Name:')
        self.project_name_label.setStyleSheet("color: #fff; font-size: 16px;")
        self.project_name_input = QLineEdit()
        self.project_name_input.setStyleSheet("background-color: #555; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        self.project_description_label = QLabel('Project description: (OPTIONAL)')
        self.project_description_label.setStyleSheet("color: #fff; font-size: 16px;")
        self.project_description_text = QPlainTextEdit()
        self.project_description_text.setStyleSheet("background-color: #555; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        def create_project_button_f(e):
            project_name = self.project_name_input.text()
            project_description = self.project_description_text.toPlainText()
            creation_date = time.ctime()
            if project_name:
                cur = self.db.cursor()
                project_path = os.path.join(pathlib.Path(__file__).parent, 'projects', project_name).__str__()
                cur.execute(f"INSERT INTO project (project_name, project_description, date_of_creation, project_path) VALUES(?,?,?,?)", (project_name, project_description, creation_date, project_path))
                cur.close()
                self.db.commit()
                self.project_name_input.setText('')
                self.project_description_text.setPlainText('')
                self.insert_into_scroll(project_name, project_description, project_path, creation_date)
                os.mkdir(os.path.join(pathlib.Path(__file__).parent, 'projects', project_name))
            else:
                msg_box = QMessageBox()
                msg_box.setStyleSheet('background-color:#333; color:#fff;')
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("Invalid project name!")
                msg_box.setWindowTitle("Error")
                msg_box.addButton("OK", QMessageBox.AcceptRole)
                msg_box.exec_()
        self.create_project_button = QPushButton("Create")
        self.create_project_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        self.create_project_button.setCursor(Qt.PointingHandCursor)
        self.create_project_button.clicked.connect(create_project_button_f)
        for element in [
            self.create_project_form_label,
            self.project_name_label,
            self.project_name_input,
            self.project_description_label,
            self.project_description_text,
            self.create_project_button
        ]: self.create_project_form_layout.addWidget(element)
        # existing projects
        self.existing_projects_label = QLabel('Your Recent Projects')
        self.existing_projects_label.setAlignment(Qt.AlignCenter)
        self.existing_projects_label.setStyleSheet("color:#fff; background-color: #333; border-radius:10px; padding:4px")
        self.existing_projects_label.setFont(QFont('arial', 20))
        self.r_layout.addWidget(self.existing_projects_label)
        self.projects_scrollarea = QScrollArea()
        self.projects_scrollarea.setStyleSheet('background-color:#333; border-radius:10px;')
        self.projects_scrollarea_widget = QWidget()
        self.projects_scrollarea.setWidget(self.projects_scrollarea_widget)
        self.projects_scrollarea.setWidgetResizable(True)
        self.projects_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.projects_scrollarea_layout = QVBoxLayout()
        self.projects_scrollarea_layout.addStretch()
        self.projects_scrollarea_widget.setLayout(self.projects_scrollarea_layout)
        self.r_layout.addWidget(self.projects_scrollarea)
        self.projects_in_db = self.seek_projects()
        for project in self.projects_in_db:
            self.insert_into_scroll(*project)

        self.show()
