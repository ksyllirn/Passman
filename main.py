from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import json
import keyring

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.db = DataBase()  
        self.new_pwd_win = AddPasswordWindow(self.db, self)
        self.show_pwd_win = AddPasswordWindow2(self.db, self)
        self.btn_add_pwd.clicked.connect(self.new_pwd_win.show)

        self.list_pwd.itemDoubleClicked.connect(self.show_pwd)

        self.update_list()

    def show_pwd(self):
        service, login = self.list_pwd.currentItem().text().split(' | ')
        password = self.db.get_password(service,login)
        self.show_pwd_win.service_edit.setText(service)
        self.show_pwd_win.login_edit.setText(login)
        self.show_pwd_win.password_edit.setText(password)
        self.show_pwd_win.show()

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
    
    def update_list(self):
        data = self.db.get_list()
        self.list_pwd.clear()
        self.list_pwd.addItems(data)


class AddPasswordWindow(QtWidgets.QWidget):
    def __init__(self, db, mw):
        super().__init__()
        self.initUI()
        self.db = db
        self.mw = mw

        self.btn_save.clicked.connect(self.add_password)

    def initUI(self):
        self.setWindowTitle('...')

        v_main = QtWidgets.QVBoxLayout()

        lbl_service = QtWidgets.QLabel('service')
        lbl_login = QtWidgets.QLabel('login')
        lbl_password = QtWidgets.QLabel('password')

        self.service_edit = QtWidgets.QLineEdit()
        self.login_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()

        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.btn_save = QtWidgets.QPushButton("save")
        
        h1 = QtWidgets.QHBoxLayout()
        h2 = QtWidgets.QHBoxLayout()
        h3 = QtWidgets.QHBoxLayout()

        h1.addWidget(lbl_service, stretch=2)
        h1.addWidget(self.service_edit, stretch=4)

        h2.addWidget(lbl_login, stretch=2)
        h2.addWidget(self.login_edit, stretch=4)

        h3.addWidget(lbl_password, stretch=2)
        h3.addWidget(self.password_edit, stretch=4)

        v_main.addLayout(h1)
        v_main.addLayout(h2)
        v_main.addLayout(h3)
        v_main.addWidget(self.btn_save, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(v_main)

    def add_password(self):
        service = self.service_edit.text()
        login = self.login_edit.text()
        password = self.password_edit.text()
        self.db.set_password(service,login,password)
        self.service_edit.clear()
        self.login_edit.clear()
        self.password_edit.clear()
        self.mw.update_list()
        self.hide()

class AddPasswordWindow2(QtWidgets.QWidget):
    def __init__(self, db, mw):
        super().__init__()
        self.initUI()
        self.db = db
        self.mw = mw

        self.btn_save.clicked.connect(self.add_password)
        self.btn_show.clicked.connect(self.show_password)

    def initUI(self):
        self.setWindowTitle('...')

        v_main = QtWidgets.QVBoxLayout()

        lbl_service = QtWidgets.QLabel('service')
        lbl_login = QtWidgets.QLabel('login')
        lbl_password = QtWidgets.QLabel('password')

        self.service_edit = QtWidgets.QLineEdit()
        self.login_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()

        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.btn_save = QtWidgets.QPushButton("save")
        self.btn_show = QtWidgets.QPushButton('👁')
        
        h1 = QtWidgets.QHBoxLayout()
        h2 = QtWidgets.QHBoxLayout()
        h3 = QtWidgets.QHBoxLayout()

        h1.addWidget(lbl_service, stretch=2)
        h1.addWidget(self.service_edit, stretch=4)

        h2.addWidget(lbl_login, stretch=2)
        h2.addWidget(self.login_edit, stretch=4)

        h3.addWidget(lbl_password, stretch=2)
        h3.addWidget(self.password_edit, stretch=4)

        v_main.addLayout(h1)
        v_main.addLayout(h2)
        v_main.addLayout(h3)
        v_main.addWidget(self.btn_save, alignment=QtCore.Qt.AlignCenter)
        v_main.addWidget(self.btn_show, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(v_main)

        self.service_edit.setReadOnly(True)
        self.login_edit.setReadOnly(True)


    def add_password(self):
        service = self.service_edit.text()
        login = self.login_edit.text()
        password = self.password_edit.text()
        self.db.set_password(service,login,password)
        self.service_edit.clear()
        self.login_edit.clear()
        self.password_edit.clear()
        self.mw.update_list()
        self.hide()

    def show_password(self):
        if self.password_edit.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

class DataBase():
    def __init__(self):
        self.filename = 'services.json'
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except:
            open(self.filename, 'w')
            self.data = dict()
    
    def set_password(self,service,login, password):
        keyring.set_password(service, login, password)
        self.data[service] = login
        with open(self.filename, 'w') as file:
            json.dump(self.data, file) 

    def get_password(self, service, login):
        return keyring.get_password(service,login)       

    def get_list(self):
        result = []
        for key in self.data:
            text = key + ' | ' + self.data[key]
            result.append(text)
        return result

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()
