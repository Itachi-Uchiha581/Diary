from voice import speak
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from secret_diary import Ui_MainWindow
import threading

conn = sqlite3.connect('credentials.db')
cursor = conn.cursor()

try:
    cursor.execute('CREATE TABLE credential (Email TEXT, Password TEXT)')
    conn.commit()
except:
    pass

class Ui_Dialoge(object):
    def open_secret_diary(self):
        self.window3 = QtWidgets.QMainWindow()
        self.ui3 = Ui_MainWindow()
        self.ui3.setupUi(self.window3)
        Dialog.hide()
        self.window3.show()
        x = threading.Thread(target=speak, args=('opening secret diary. Now you can write here safely and securely',))
        x.start()
    def login_system(self):
        email_value = self.email_log_in_plain_text.text()
        password_value = self.password_log_in_plain_text.text()

        cursor.execute('SELECT * FROM credential')
        items = cursor.fetchall()
        if len(items) == 0:
            cursor.execute('INSERT INTO credential (Email, Password) VALUES (?, ?)', (email_value, password_value))
            conn.commit()
            self.email_log_in_plain_text.setText('')
            self.password_log_in_plain_text.setText('')
            speak('Successfully signed up. Please enter you credentials again to log in')

        else:
            if items[0][0] == email_value and items[0][1] == password_value:
                self.open_secret_diary()
                x = threading.Thread(target=speak,args=('User identified. Welcome Now you can access you secret diary',))
                x.start()

            else:
                speak('Wrong Credentials. Please Try again')


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(641, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.email_log_in_label = QtWidgets.QLabel(Dialog)
        self.email_log_in_label.setGeometry(QtCore.QRect(110, 120, 181, 81))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.email_log_in_label.setFont(font)
        self.email_log_in_label.setObjectName("email_log_in_label")
        self.password_log_in_label = QtWidgets.QLabel(Dialog)
        self.password_log_in_label.setGeometry(QtCore.QRect(110, 210, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.password_log_in_label.setFont(font)
        self.password_log_in_label.setObjectName("password_log_in_label")
        self.email_log_in_plain_text = QtWidgets.QLineEdit(Dialog)
        self.email_log_in_plain_text.setGeometry(QtCore.QRect(300, 150, 211, 31))
        self.email_log_in_plain_text.setObjectName("email_log_in_plain_text")
        self.email_log_in_plain_text.setPlaceholderText('Email')
        self.password_log_in_plain_text = QtWidgets.QLineEdit(Dialog)
        self.password_log_in_plain_text.setGeometry(QtCore.QRect(350, 240, 191, 31))
        self.password_log_in_plain_text.setObjectName("password_log_in_plain_text")
        self.password_log_in_plain_text.setPlaceholderText('Password')
        self.password_log_in_plain_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.log_in_button = QtWidgets.QPushButton(Dialog)
        self.log_in_button.setGeometry(QtCore.QRect(290, 350, 75, 23))
        self.log_in_button.setAutoFillBackground(False)
        self.log_in_button.setStyleSheet("background-color: rgb(131, 193, 202)")
        self.log_in_button.setDefault(False)
        self.log_in_button.setFlat(False)
        self.log_in_button.setObjectName("log_in_button")
        self.log_in_button.clicked.connect(self.login_system)
        self.invalid_user_name_or_password = QtWidgets.QLabel(Dialog)
        self.invalid_user_name_or_password.setGeometry(QtCore.QRect(310, 320, 47, 13))
        self.invalid_user_name_or_password.setText("")
        self.invalid_user_name_or_password.setObjectName("invalid_user_name_or_password")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.email_log_in_label.setText(_translate("Dialog", "Email"))
        self.password_log_in_label.setText(_translate("Dialog", "Password"))
        self.log_in_button.setText(_translate("Dialog", "Log in"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialoge()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
