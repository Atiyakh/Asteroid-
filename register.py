from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os, pathlib
from project import WelcomePage

def ClearLayout(layout):
    for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().setParent(None)

class Main(QMainWindow):
    def __init__(self):
        # config
        super(Main, self).__init__()
        self.setStyleSheet("background-color: #222;")
        self.setWindowTitle("AstroCode - Registration Page")
        self.setWindowIcon(QIcon(os.path.join(pathlib.Path(__file__).parent, 'static', 'black_icon.png')))
        self.window_width, self.window_height = 783, 550
        self.setFixedSize(QSize(self.window_width, self.window_height))
        # widgets
        self.window_layout = QHBoxLayout()
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        self.window_widget = QWidget()
        self.window_widget.setLayout(self.window_layout)
        self.setCentralWidget(self.window_widget)
        # nav
        self.nav_widget = QWidget()
        self.nav_widget.setFixedWidth(int(self.window_width * 0.35))
        self.nav_layout = QVBoxLayout()
        self.nav_widget.setLayout(self.nav_layout)
        self.window_layout.addWidget(self.nav_widget)
        self.nav_widget.setStyleSheet('''
QWidget{
    background-color: #333;
}
QPushButton{
    background-color: #333;
    color: #fff;
    font-size: 25px;
    padding: 4px;
    border-radius: 5px;
    border-width: 0px;
}
QPushButton:hover{
    background-color: #444;
    color: #fff;
    font-size: 25px;
    padding: 4px;
    border-radius: 5px;
    border-width: 0px;
}''')
        self.main_window_widget = QWidget()
        self.main_window_widget.setStyleSheet("background-color: #222;")
        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.setAlignment(Qt.AlignCenter)
        self.main_window_widget.setLayout(self.main_window_layout)
        self.window_layout.addWidget(self.main_window_widget)
        # astroweb trademark
        self.astro_trademark = QWidget()
        self.astro_trademark_layout = QVBoxLayout()
        self.astro_trademark.setLayout(self.astro_trademark_layout)
        self.astro_icon = QPushButton()
        self.astro_icon.setIcon(QIcon(os.path.join(pathlib.Path(__file__).parent, 'static', 'colored_icon.png')))
        self.astro_icon.setStyleSheet("background-color: #333; color: #fff; font-size: 25px; padding: 4px; border-radius: 5px; border-width: 0px;")
        self.astro_icon.setIconSize(QSize(130, 130))
        self.astro_brandname = QLabel("AstroCode")
        self.astro_brandname.setAlignment(Qt.AlignCenter)
        self.astro_brandname.setStyleSheet("color: #75a1ff;")
        font = QFont("Helvetica", 25)
        self.astro_brandname.setFont(font)
        self.nav_layout.addWidget(self.astro_trademark)
        self.astro_trademark_layout.addWidget(self.astro_icon)
        self.astro_trademark_layout.addWidget(self.astro_brandname)
        self.border_frame = QWidget()
        self.border_frame.setFixedHeight(1)
        self.border_frame.setStyleSheet("background-color: #999;")
        # login page
        self.login_widget = QWidget()
        self.login_widget.setStyleSheet('background-color: #333; border-color: #555; border-width:1px; border-style:solid; border-radius:10px;')
        self.login_widget.setFixedSize(QSize(int(self.main_window_widget.width() * 0.55), int(self.main_window_widget.height())))
        self.login_layout = QVBoxLayout()
        self.login_widget.setLayout(self.login_layout)
        self.login_label = QLabel("Login Form")
        self.login_label.setFont(QFont("Helvetica"))
        self.login_layout.addWidget(self.login_label)
        self.login_label.setStyleSheet(
            "color:#fff; font-size:36px; border-color: #333;")
        self.login_label.setFixedHeight(60)
        self.login_label.setAlignment(Qt.AlignCenter)
        self.label_img = QPushButton()
        self.label_img.setStyleSheet("border-color:#333;")
        self.label_img.setIcon(QIcon("static\\login.png"))
        self.label_img.setIconSize(QSize(180, 180))
        self.login_layout.addWidget(self.label_img)
        self.name_e = QLineEdit()
        self.name_e.setFont(QFont("Helvetica"))
        self.name_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.name_e.setPlaceholderText("Username")
        self.login_layout.addWidget(self.name_e)
        self.pass_e = QLineEdit()
        self.pass_e.setFont(QFont("Helvetica"))
        self.pass_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.pass_e.setPlaceholderText("Password")
        self.pass_e.setEchoMode(QLineEdit.Password)
        self.login_layout.addWidget(self.pass_e)
        def submit_button_f(e):
            self.enter_to_project()
        self.submit_button = QPushButton("Login")
        self.submit_button.setFont(QFont("Helvetica"))
        self.submit_button.clicked.connect(submit_button_f)
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.setStyleSheet(
            "color: #fff; background-color: #1F7BFF; padding: 6px; border-radius:15px; font-size: 16px; border-color: #1F7BFF")
        self.login_layout.addWidget(self.submit_button)
        # signup page
        self.signup_widget = QWidget()
        self.signup_widget.setStyleSheet('background-color: #333; border-color: #555; border-width:1px; border-style:solid; border-radius:10px;')
        self.signup_widget.setFixedSize(QSize(int(self.main_window_widget.width() * 0.55), int(self.main_window_widget.height())))
        self.signup_layout = QVBoxLayout()
        self.signup_widget.setLayout(self.signup_layout)
        self.signup_label = QLabel("Signup Form")
        self.signup_label.setFont(QFont("Helvetica"))
        self.signup_layout.addWidget(self.signup_label)
        self.signup_label.setStyleSheet(
            "color:#fff; font-size:36px; border-color: #333;")
        self.signup_label.setFixedHeight(60)
        self.signup_label.setAlignment(Qt.AlignCenter)
        self.signup_label_img = QPushButton()
        self.signup_label_img.setStyleSheet("border-color:#333;")
        self.signup_label_img.setIcon(QIcon("static\\login.png"))
        self.signup_label_img.setIconSize(QSize(180, 180))
        self.signup_layout.addWidget(self.signup_label_img)
        self.signup_name_e = QLineEdit()
        self.signup_label.setFont(QFont("Helvetica"))
        self.signup_name_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.signup_name_e.setPlaceholderText("Username")
        self.signup_layout.addWidget(self.signup_name_e)
        self.signup_pass_e = QLineEdit()
        self.signup_pass_e.setFont(QFont("Helvetica"))
        self.signup_pass_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.signup_pass_e.setPlaceholderText("Password")
        self.signup_pass_e.setEchoMode(QLineEdit.Password)
        self.signup_layout.addWidget(self.signup_pass_e)
        def signup_submit_button_f(e):
            print("Hello")
        self.signup_submit_button = QPushButton("signup")
        self.signup_submit_button.setFont(QFont("Helvetica"))
        self.signup_submit_button.clicked.connect(signup_submit_button_f)
        self.signup_submit_button.setCursor(Qt.PointingHandCursor)
        self.signup_submit_button.setStyleSheet(
            "color: #fff; background-color: #1F7BFF; padding: 6px; border-radius:15px; font-size: 16px; border-color: #1F7BFF")
        self.signup_layout.addWidget(self.signup_submit_button)
        # contact us
        self.contactus_widget = QWidget()
        self.contactus_widget.setStyleSheet('background-color: #333; border-color: #555; border-width:1px; border-style:solid; border-radius:10px;')
        self.contactus_widget.setFixedSize(QSize(int(self.main_window_widget.width() * 0.55), int(self.main_window_widget.height())))
        self.contactus_layout = QVBoxLayout()
        self.contactus_widget.setLayout(self.contactus_layout)
        self.contactus_label = QLabel("Contact us")
        self.contactus_layout.addWidget(self.contactus_label)
        self.contactus_label.setStyleSheet(
            "color:#fff; font-size:36px; border-color: #333;")
        self.contactus_label.setFixedHeight(60)
        self.contactus_label.setFont(QFont("Helvetica"))
        self.contactus_label.setAlignment(Qt.AlignCenter)
        self.contactus_name_e = QLineEdit()
        self.contactus_name_e.setFont(QFont("Helvetica"))
        self.contactus_name_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.contactus_name_e.setPlaceholderText("Full Name")
        self.contactus_layout.addWidget(self.contactus_name_e)
        self.contactus_email_e = QLineEdit()
        self.contactus_email_e.setFont(QFont("Helvetica"))
        self.contactus_email_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.contactus_email_e.setPlaceholderText("Email")
        self.contactus_layout.addWidget(self.contactus_email_e)
        self.contactus_message_ptext = QPlainTextEdit()
        self.contactus_message_ptext.setFont(QFont("Helvetica"))
        self.contactus_message_ptext.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.contactus_message_ptext.setPlaceholderText("Message")
        self.contactus_layout.addWidget(self.contactus_message_ptext)
        self.contactus_submit_button = QPushButton("Send Message")
        self.contactus_submit_button.clicked.connect(signup_submit_button_f)
        self.contactus_submit_button.setCursor(Qt.PointingHandCursor)
        self.contactus_submit_button.setStyleSheet(
            "color: #fff; background-color: #1F7BFF; padding: 6px; border-radius:15px; font-size: 16px; border-color: #1F7BFF")
        self.contactus_layout.addWidget(self.contactus_submit_button)
        # navigations
        def switch_navigations(_):
            _nav = self.focusWidget()
            ClearLayout(self.main_window_layout)
            self.main_window_layout.addWidget(self.navigations[_nav])
            for nav in self.navigations:
                if nav == _nav:
                    nav.setStyleSheet("""
QPushButton{
    background-color: #444;
    color: #75a1ff;
    font-size: 25px;
    padding: 4px;
    border-radius: 5px;
    border-width: 0px;
}""")
                else:
                    nav.setStyleSheet("""
QPushButton{
    background-color: #333;
    color: #fff;
    font-size: 25px;
    padding: 4px;
    border-radius: 5px;
    border-width: 0px;
}
QPushButton:hover{
    background-color: #444;
    color: #fff;
    font-size: 25px;
    padding: 4px;
    border-radius: 5px;
    border-width: 0px;
}""")
        self.login_nav = QPushButton("Log in")
        self.nav_layout.addWidget(self.login_nav)
        self.login_nav.setCursor(Qt.PointingHandCursor)
        self.signup_nav = QPushButton("Sign up")
        self.nav_layout.addWidget(self.signup_nav)
        self.signup_nav.setCursor(Qt.PointingHandCursor)
        self.contact_us_nav = QPushButton("Contact us")
        self.nav_layout.addWidget(self.contact_us_nav)
        self.contact_us_nav.setCursor(Qt.PointingHandCursor)
        self.nav_layout.addStretch()
        self.text_label = QLabel("AstroCode V1 github.com/Atiyakh/AstroCode/")
        self.text_label.setStyleSheet('color: #fff;')
        self.text_label.setAlignment(Qt.AlignCenter)
        self.nav_layout.addWidget(self.text_label)
        self.navigations = {
            self.signup_nav: self.signup_widget,
            self.login_nav: self.login_widget,
            self.contact_us_nav: self.contactus_widget
        }
        for nav in self.navigations:
            nav.setFont(QFont("Helvetica"))
            nav.clicked.connect(switch_navigations)
        self.main_window_layout.addWidget(self.login_widget)
        self.login_nav.setStyleSheet("""
QPushButton{
    background-color: #444;
    color: #75a1ff;
    font-size: 25px;
    padding: 4px;
    border-radius: 5px;
    border-width: 0px;
}""")

        self.show()
    def enter_to_project(self):
        self.welcome_page = WelcomePage()
        self.setCentralWidget(self.welcome_page)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Main()
    window.app_ = application
    application.exec_()
