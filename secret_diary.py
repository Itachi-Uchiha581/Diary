from voice import speak
import sys
import sqlite3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *


conn = sqlite3.connect('diary_data')
cursor = conn.cursor()

try:
    cursor.execute('CREATE TABLE warehouse (diary_data TEXT, page_number INTEGER NOT NULL UNIQUE)')
    conn.commit()
except:
    pass


class Ui_MainWindow(object):
    def next_page(self):
        self.page_number_display.display(self.page_number+1)
        self.page_number = self.page_number + 1

    def previous_page(self):
        if self.page_number == 1:
            speak('You can not go below this page')
        else:
            self.page_number_display.display(self.page_number - 1)
            self.page_number = self.page_number - 1

    def log_out(self):
        sys.exit(0)

    def save_data(self):
        diary_data = self.diary_writing_plain_text.toPlainText()

        try:
            cursor.execute('INSERT INTO warehouse (diary_data, page_number) VALUES (?, ?)', (diary_data, self.page_number))
            conn.commit()
        except:
            cursor.execute('UPDATE warehouse SET diary_data = ? WHERE page_number = ?', (diary_data, self.page_number))
            conn.commit()

    def load_data(self):
        try:
            cursor.execute('SELECT diary_data FROM warehouse WHERE page_number = ?', str(self.page_number))
            item = cursor.fetchone()
            conn.commit()
            self.diary_writing_plain_text.setPlainText(item[0])
        except:
            self.diary_writing_plain_text.setPlainText('')
            speak('No data available in this Page')

    def encrypt_func(self):
        def caesar_encrypt(word):
            c = ''
            for i in word:
                if (i == ' '):
                    c += ' '
                else:
                    c += (chr(ord(i) + 3))
            return c
        self.diary_writing_plain_text.setPlainText(caesar_encrypt(self.diary_writing_plain_text.toPlainText()))

    def decrypt_func(self):
        def caesar_decrypt(word):
            c = ''
            for i in word:
                if (i == ' '):
                    c += ' '
                else:
                    c += (chr(ord(i) - 3))
            return c
        self.diary_writing_plain_text.setPlainText(caesar_decrypt(self.diary_writing_plain_text.toPlainText()))



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(641, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.diary_writing_plain_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.diary_writing_plain_text.setGeometry(QtCore.QRect(0, 0, 471, 431))
        self.diary_writing_plain_text.setObjectName("diary_writing_plain_text")
        my_font = QFont()
        my_font.setBold(True)
        my_font.setPointSize(12)
        self.diary_writing_plain_text.setFont(my_font)
        self.diary_writing_plain_text.setPlaceholderText('Write HERE!')
        self.next_page_btn = QtWidgets.QPushButton(self.centralwidget)
        self.next_page_btn.setGeometry(QtCore.QRect(480, 20, 75, 23))
        self.next_page_btn.setObjectName("next_page_btn")
        self.next_page_btn.clicked.connect(self.next_page)
        self.previous_page_btn = QtWidgets.QPushButton(self.centralwidget)
        self.previous_page_btn.setGeometry(QtCore.QRect(480, 110, 81, 23))
        self.previous_page_btn.setObjectName("previous_page_btn")
        self.previous_page_btn.clicked.connect(self.previous_page)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(480, 160, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.encrypt_func)
        self.page_number_display = QtWidgets.QLCDNumber(self.centralwidget)
        self.page_number_display.setGeometry(QtCore.QRect(490, 60, 64, 23))
        self.page_number_display.setStyleSheet("background-color: black")
        self.page_number_display.setObjectName("page_number_display")
        self.page_number = 1
        self.page_number_display.display(self.page_number)
        self.decrypt_btn = QtWidgets.QPushButton(self.centralwidget)
        self.decrypt_btn.setGeometry(QtCore.QRect(480, 200, 75, 23))
        self.decrypt_btn.setObjectName("decrypt_btn")
        self.decrypt_btn.clicked.connect(self.decrypt_func)
        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setGeometry(480, 240, 75, 23)
        self.load_btn.setObjectName("load_btn")
        self.load_btn.clicked.connect(self.load_data)
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(480, 280, 75, 23)
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_data)
        self.log_out_btn = QtWidgets.QPushButton(self.centralwidget)
        self.log_out_btn.setGeometry(QtCore.QRect(560, 410, 75, 23))
        self.log_out_btn.setObjectName("log_out_btn")
        self.log_out_btn.clicked.connect(self.log_out)
        self.date_secret_diary = QtWidgets.QLabel(self.centralwidget)
        self.date_secret_diary.setGeometry(QtCore.QRect(500, 290, 121, 20))
        self.date_secret_diary.setText("")
        self.date_secret_diary.setObjectName("date_secret_diary")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 641, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.next_page_btn.setText(_translate("MainWindow", "Next Page"))
        self.previous_page_btn.setText(_translate("MainWindow", "Previous Page"))
        self.pushButton_3.setText(_translate("MainWindow", "Encrypt"))
        self.decrypt_btn.setText(_translate("MainWindow", "Decrypt"))
        self.load_btn.setText(_translate("MainWindow", "Load"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.log_out_btn.setText(_translate("MainWindow", "Log out"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
