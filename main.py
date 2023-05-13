from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        self.setWindowTitle('Passman')

        #topbar
        h_topbar = QtWidgets.QHBoxLayout()
        top_bar = QtWidgets.QFrame()
        self.btn_add_pwd = QtWidgets.QPushButton("add password")
        h_topbar.addStretch(6)
        h_topbar.addWidget(self.btn_add_pwd,stretch=2)
        top_bar.setLayout(h_topbar)

        #password list
        self.list_pwd = QtWidgets.QListWidget()

        #main
        v_main = QtWidgets.QVBoxLayout()
        v_main.addWidget(top_bar)
        v_main.addWidget(self.list_pwd)

        self.setLayout(v_main)
    

class AddPasswordWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        v_main = QtWidgets.QVBoxLayout()

        lbl_service = QtWidgets.QLabel('service')
        lbl_login = QtWidgets.QLabel('login')
        lbl_password = QtWidgets.QLabel('password')

        self.service_edit = QtWidgets.QLineEdit()
        self.login_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()

        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()
