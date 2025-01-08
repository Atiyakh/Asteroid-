from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, time


class GUI(QMainWindow):
    def mousePressEvent(self, event):
        try:
            self.oldPosition = event.globalPos()
        except:
            pass

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            pass

    def InsertMessage(self, sender, message):
        # msg layout:
        msg_w = QWidget()
        msg_w_l = QVBoxLayout()
        msg_w.setLayout(msg_w_l)
        # message body:
        msg_label = QLabel()
        msg_label.setMaximumWidth(250)
        if sender == self.username:
            alg = Qt.AlignLeft
            bg = "#1F7BFF"
        else:
            alg = Qt.AlignRight
            bg = "#555"
        msg_label.setStyleSheet(
            f"font-size:16px; color: #fff; background-color:{bg}; border-color:{bg}; padding:3px;")
        msg_label.setWordWrap(True)
        msg_label.setText(message)
        self.testing_label.setText(message)
        self.testing_label.adjustSize()
        msg_label.setFixedSize(self.testing_label.width(),
                               self.testing_label.height())
        msg_w_l.addWidget(msg_label, alignment=alg)
        # sender:
        sender_label = QLabel(sender+f" {time.ctime()}")
        sender_label.setMaximumWidth(250)
        sender_label.setStyleSheet("font-size:11px; color: #fff")
        if sender == self.username:
            alg = Qt.AlignLeft
        else:
            alg = Qt.AlignRight
        msg_w_l.addWidget(sender_label, alignment=alg)
        # insert message:
        if sender == self.username:
            x = 0
        else:
            x = 1
        self.chatroom_layout.addWidget(msg_w, self.chatroom_layout.count()-1, x)
        self.chatroom_sa.verticalScrollBar().setValue(self.chatroom_sa.verticalScrollBar().maximum())
    def initui(self):
        # ChatRoom:
        def test_button_f(e):
            self.InsertMessage(*self.test_button.data)
        self.test_button = QPushButton()
        # self.server.server.Requests.Communication.button = self.test_button
        self.test_button.clicked.connect(test_button_f)
        self.testing_label = QLabel()
        self.testing_label.setStyleSheet(
            f"font-size:16px; color: #fff; background-color:red; border-color:red; padding:3px;")
        self.testing_label.setWordWrap(True)
        self.testing_label.setMaximumWidth(250)
        self.chat_room_page = QWidget()
        self.chat_room_layout = QVBoxLayout()
        self.chat_room_page.setLayout(self.chat_room_layout)
        self.chat_room_page.setStyleSheet(
            'background-color: #222; border-color: #555; border-width:1px; border-style:solid; border-radius:10px;')
        self.label_chatroom = QLabel("Chat Room")
        self.label_chatroom.setAlignment(Qt.AlignCenter)
        self.label_chatroom.setStyleSheet(
            "color:#fff; font-size:25px; border-color: #222")
        self.label_chatroom.setFixedHeight(60)
        self.chatroom_sa = QScrollArea()
        self.chatroom_sa.setStyleSheet("""
QScrollBar {
  background: #222;
  border-radius: 5px;
  width:10px;
}

QScrollBar::handle {
  background-color: #1F7BFF;
  border-radius: 3px;
}""")
        self.chatroom = QWidget()
        self.chatroom.setStyleSheet("border-color:#222;")
        self.chatroom_sa.setWidget(self.chatroom)
        self.chatroom_sa.setWidgetResizable(True)
        self.chatroom_layout = QGridLayout()
        self.chatroom_layout.addWidget(QWidget())
        self.chatroom.setLayout(self.chatroom_layout)

        def msg_e_f():
            if self.msg_e.text():
                self.server.send_msg(self.username, self.msg_e.text())
                self.msg_e.setText("")
        self.msg_e = QLineEdit()
        self.msg_e.returnPressed.connect(msg_e_f)
        self.msg_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #6999ff; border-width:3px; border-radius:18px; padding:6px;")
        self.msg_e.setPlaceholderText("Type your message")
        self.chat_room_layout.addWidget(self.label_chatroom)
        self.chat_room_layout.addWidget(self.chatroom_sa)
        self.chat_room_layout.addWidget(self.msg_e)
        # Signup:
        self.setFixedSize(360, 400)
        self.signin_page = QWidget()
        self.setCentralWidget(self.signin_page)
        self.centralWidget().setStyleSheet(
            'background-color: #222; border-color: #555; border-width:1px; border-style:solid; border-radius:10px;')
        self.signin_layout = QVBoxLayout()
        self.signin_page.setLayout(self.signin_layout)
        self.login_label = QLabel("Login Page")
        self.login_label.setStyleSheet(
            "color:#fff; font-size:36px; border-color: #222;")
        self.login_label.setFixedHeight(60)
        self.login_label.setAlignment(Qt.AlignCenter)
        self.label_img = QPushButton()
        self.label_img.setStyleSheet("border-color:#222;")
        self.label_img.setIcon(QIcon("static\\login.png"))
        self.label_img.setIconSize(QSize(180, 180))
        self.name_e = QLineEdit()
        self.name_e.setFixedWidth(340)
        self.name_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.name_e.setPlaceholderText("Username")
        self.pass_e = QLineEdit()
        self.pass_e.setStyleSheet(
            "color:#fff; font-size:16px; border-color: #1F7BFF; border-width:3px; border-radius:18px; padding:6px;")
        self.pass_e.setFixedWidth(340)
        self.pass_e.setPlaceholderText("Password")
        self.pass_e.setEchoMode(QLineEdit.Password)

        def submit_button_f(e):
            self.username = self.name_e.text()
            response = self.server.login(
                self.name_e.text(),
                self.pass_e.text()
            )
            if response:
                self.setFixedWidth(520)
                self.setCentralWidget(self.chat_room_page)
        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(submit_button_f)
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.setStyleSheet(
            "color: #fff; background-color: #1F7BFF; padding: 6px; border-radius:15px; font-size: 16px; border-color: #1F7BFF")
        self.submit_button.setFixedWidth(200)
        for widget in [self.login_label, self.label_img, self.name_e, self.pass_e, self.submit_button]:
            self.signin_layout.addWidget(widget, alignment=Qt.AlignCenter)
        self.show()

    def __init__(self, mainclass):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.server = mainclass
        self.initui()
        self.app.exec_()

if __name__ == '__main__':
    app = QApplication([])
    gui = GUI(1)
    app.exec_()
