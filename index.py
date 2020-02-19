# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from random import randint
from sys import exit , argv
import sqlite3
from yagmail import SMTP

main_ui,_ = loadUiType("Login.ui")

class Main(QMainWindow , main_ui):

    sq = sqlite3.connect('data.db')
    cur = sq.cursor()
    code = randint(111111 , 999999)

    def __init__(self , parent = None):
        super(Main , self).__init__( parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI_Changes()
        self.Handel_Buttons()

    def UI_Changes(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.signup)
        self.pushButton_3.clicked.connect(self.add_user)
        self.pushButton_4.clicked.connect(self.reset)
        self.pushButton_5.clicked.connect(self.check_code)
        self.pushButton_6.clicked.connect(self.change_pass)
        self.pushButton_7.clicked.connect(self.forget_win)
        self.pushButton_8.clicked.connect(self.loginwin)
        self.pushButton_9.clicked.connect(self.loginwin)
        self.pushButton_10.clicked.connect(self.forget_win)
        self.pushButton_11.clicked.connect(self.send_code)


    def login(self):
        self.cur.execute("select username , pass , email from Users where username  = '{}' or email = '{}' " .format(self.lineEdit.text() , self.lineEdit.text()))
        data = self.cur.fetchall()
        allpass = []
        alluser = []
        for i in data:
            allpass.append(i[1])

        for m in data:
            alluser.append(i[0])
            alluser.append(i[2])

        check = [self.lineEdit_2.text() , self.lineEdit.text()]
        if all(check) == True:
            if self.lineEdit.text() in alluser:
                if self.lineEdit_2.text() in allpass :
                    QMessageBox.information(self , 'Login Info' , 'Login Succ But This Window Not Finshed Yet .. ')

                else:
                    QMessageBox.information(self , 'Password Error' , 'Check From Password Pls')
            else :
                QMessageBox.information(self, 'Email Or User Error', 'Check From Email Or Username Pls')
        else:
            QMessageBox.information(self , 'Filed Forget' , "Pls Check From Fileds ..")

    def reset(self):
        self.cur.execute('select email from Users')
        data = self.cur.fetchall()
        allemail = []
        for row in data :
            for h in row:
                allemail.append(h)
        if self.lineEdit_7.text() in allemail :
            SMTP({"You Email": "Username"}, "YouPass").send(self.lineEdit_7.text(), "Loger App Reset Password" , "A password reset for your account was requested Code Is : {}".format(self.code))
            self.tabWidget.setCurrentIndex(3)

        else:
            QMessageBox.information(self , 'Email Error' , "This Email Not Found ..")

    def loginwin(self):
        self.tabWidget.setCurrentIndex(0)

    def forget_win(self):
        self.tabWidget.setCurrentIndex(2)

    def code_win(self):
        self.tabWidget.setCurrentIndex(3)

    def signup(self):
        self.tabWidget.setCurrentIndex(1)

    def new_pass(self):
        self.tabWidget.setCurrentIndex(4)

    def check_code(self):
        if self.lineEdit_9.text() == str(self.code) :
            self.tabWidget.setCurrentIndex(4)

    def send_code(self):
        self.code = randint(111111 , 999999)
        SMTP({"Your Email": "USerName"}, "Password").send(self.lineEdit_7.text(),
                                                                             "Loger App Reset Password",
                                                                             "A password reset for your account was requested Code Is : {}".format(
                                                                                 self.code))

    def change_pass(self):
        pass1 = self.lineEdit_10.text()
        pass2 = self.lineEdit_11.text()
        if pass1 == pass2 :
            if len(pass1) >= 8 :
                self.cur.execute("update Users set pass = '{}' where email = '{}' ".format(pass1 , self.lineEdit_7.text()))
                self.sq.commit()
                self.lineEdit_10.setText("")
                self.lineEdit_11.setText("")
                QMessageBox.information(self , 'Password Information' , 'Password Change')
                self.tabWidget.setCurrentIndex(0)
            else:
                QMessageBox.information(self , 'Password Erroe' , 'Password Should More Than 7 charcter')
        else:
            QMessageBox.information(self , 'Password Error' , 'The Password Should Be Same ')
    def add_user(self):
        name = self.lineEdit_3.text()
        email = self.lineEdit_5.text()
        username = self.lineEdit_4.text()
        password = self.lineEdit_6.text()
        password2 = self.lineEdit_8.text()
        lis = [name , email , username , password , password2]
        self.cur.execute('select username , email from Users')
        data = self.cur.fetchall()
        alluser = []
        allemail = []
        for user in data :
                alluser.append(user[0])
                allemail.append(user[1])

        if all(lis) == True:
            if email not in allemail or username not in alluser:
                if password == password2 :
                    if len(password) >= 8 :
                        try:
                            self.cur.execute("""insert into Users (name , email , pass , username) values('{}' , '{}' , '{}' , '{}')""".format(name , email , password , username))
                            self.sq.commit()
                            self.add_user()
                            QMessageBox.information(self , 'User Add ' , 'User Add to Our DataBase')
                            self.lineEdit_3.setText("")
                            self.lineEdit_5.setText("")
                            self.lineEdit_4.setText("")
                            self.lineEdit_6.setText("")
                            self.lineEdit_8.setText("")
                        except Exception:
                            if email in allemail:
                                QMessageBox.information(self, 'Email Error', 'This Email Uesd Pls Try Anthor Email')
                            elif username in alluser:
                                QMessageBox.information(self, 'Username Error',
                                                        'This Username Uesd Pls Try Anthor Username')
                    else :
                        QMessageBox.information(self , 'Password Error' , 'Passwword should be more than 8 charcter')
                else :
                    QMessageBox.information(self , 'Password Error' , "Check From Pass Pls")
            else:
                if email in allemail:
                    counter = 1
                    if counter != 1 :
                        QMessageBox.information(self , 'Email Error' , 'This Email Uesd Pls Try Anthor Email')
                        counter += 1
                else:
                    QMessageBox.information(self , 'Username Error' , 'This Username Uesd Pls Try Anthor Username')

        else:
            QMessageBox.about(self , 'Error' , 'You Forget Fileds' )

def main():
    app = QApplication(argv)
    window = Main()
    window.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
