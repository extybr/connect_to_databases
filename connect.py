import os.path
import database
from PyQt5 import QtWidgets
from gui import UiForm
from config import *


class MyWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiForm()
        self.ui.setup_ui(self)
        self.ui.pushButton_2.clicked.connect(self.set_config)
        self.ui.pushButton.clicked.connect(self.get_data)

    def set_config(self) -> None:
        """ My configuration """
        if self.ui.comboButton.currentIndex() == 1:
            self.ui.lineEdit.setText('')
            self.ui.lineEdit_2.setText('')
            self.ui.lineEdit_3.setText('')
            self.ui.lineEdit_4.setText('')
            self.ui.lineEdit_5.setText(DB_SQLITE)
            self.ui.lineEdit_6.setText(TABLE_SQLITE)
        elif self.ui.comboButton.currentIndex() == 2:
            self.ui.lineEdit.setText(HOST)
            self.ui.lineEdit_2.setText(PORT_POSTGRESQL)
            self.ui.lineEdit_3.setText(USER_POSTGRESQL)
            self.ui.lineEdit_4.setText(DB_PASSWORD)
            self.ui.lineEdit_5.setText(DB_POSTGRESQL)
            self.ui.lineEdit_6.setText(TABLE_POSTGRESQL)
        elif self.ui.comboButton.currentIndex() == 3:
            self.ui.lineEdit.setText(HOST)
            self.ui.lineEdit_2.setText(PORT_MYSQL)
            self.ui.lineEdit_3.setText(USER_MYSQL)
            self.ui.lineEdit_4.setText(DB_PASSWORD)
            self.ui.lineEdit_5.setText(DB_MYSQL)
            self.ui.lineEdit_6.setText(TABLE_MYSQL)
        elif self.ui.comboButton.currentIndex() == 4:
            self.ui.lineEdit.setText(HOST)
            self.ui.lineEdit_2.setText(PORT_MSSQL)
            self.ui.lineEdit_3.setText(USER_MSSQL)
            self.ui.lineEdit_4.setText('')
            self.ui.lineEdit_5.setText('')
            self.ui.lineEdit_6.setText('')

    def get_data(self) -> None:
        """ Output data """
        try:
            self.ui.textBrowser.clear()
            output = '😍'.center(105, '*').split('\t')
            if self.ui.radioButton.isChecked():
                if os.path.exists(self.ui.lineEdit_5.displayText()) or (
                        self.ui.lineEdit_7.displayText().split(' ')[0].lower() == 'create'):
                    output = database.read_sqlite3(self.ui.lineEdit_5.displayText(),
                                                   self.ui.lineEdit_6.displayText(),
                                                   self.ui.lineEdit_7.displayText())
                else:
                    self.ui.textBrowser.append(
                        '\n\n' + '  База Данных отсутствует  '.center(109, '*'))
                    files = []
                    extension = ['.db', '.sdb', '.sqlite', '.db3', '.s3db', 'sqlite3', '.sl3']
                    for file in os.listdir(os.getcwd()):
                        if [i for i in extension if file.strip().endswith(i) or
                           file.strip().endswith(i.upper())]:
                            files.append(file)
                    if len(files) > 0:
                        self.ui.textBrowser.append(f'\nНо есть эти базы - {files}\n')
            elif self.ui.radioButton_2.isChecked():
                output = database.read_postgresql(self.ui.lineEdit.displayText(),
                                                  int(self.ui.lineEdit_2.displayText()),
                                                  self.ui.lineEdit_3.displayText(),
                                                  self.ui.lineEdit_4.displayText(),
                                                  self.ui.lineEdit_5.displayText(),
                                                  self.ui.lineEdit_6.displayText(),
                                                  self.ui.lineEdit_7.displayText())
            elif self.ui.radioButton_3.isChecked():
                output = database.read_mysql(self.ui.lineEdit.displayText(),
                                             int(self.ui.lineEdit_2.displayText()),
                                             self.ui.lineEdit_3.displayText(),
                                             self.ui.lineEdit_4.displayText(),
                                             self.ui.lineEdit_5.displayText(),
                                             self.ui.lineEdit_6.displayText(),
                                             self.ui.lineEdit_7.displayText())
            elif self.ui.radioButton_4.isChecked():
                output = database.read_mssql(self.ui.lineEdit.displayText(),
                                             int(self.ui.lineEdit_2.displayText()),
                                             self.ui.lineEdit_3.displayText(),
                                             self.ui.lineEdit_4.displayText(),
                                             self.ui.lineEdit_5.displayText(),
                                             self.ui.lineEdit_6.displayText(),
                                             self.ui.lineEdit_7.displayText())
            for line in output:
                self.ui.textBrowser.append(line)
            self.ui.textBrowser.scrollToAnchor("scroll")
        except Exception as error:
            self.ui.textBrowser.append(f'{error}')
