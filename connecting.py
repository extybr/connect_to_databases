import os.path
from database import Database
from PyQt5 import QtWidgets
from gui import UiForm


class MyWin(QtWidgets.QWidget, Database):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = UiForm()
        self.ui.setup_ui(self)
        self.ui.pushButton.clicked.connect(self.get_data)

    def get_data(self) -> None:
        try:
            self.ui.textBrowser.clear()
            output = '😍'.center(105, '*').split('\t')
            if self.ui.radioButton.isChecked():
                if os.path.exists(self.ui.lineEdit_5.displayText()):
                    output = self.read_database_sqllite3(self.ui.lineEdit_5.displayText(),
                                                         self.ui.lineEdit_6.displayText())
                else:
                    self.ui.textBrowser.append(
                        '\n\n' + '  База Данных отсутствует  '.center(109, '*'))
                    files = []
                    for file in os.listdir(os.getcwd()):
                        if file.endswith('.db'):
                            files.append(file)
                    if len(files) > 0:
                        self.ui.textBrowser.append(f'\nНо есть эти базы - {files}\n')
            elif self.ui.radioButton_2.isChecked():
                output = self.read_database_postgresql(self.ui.lineEdit.displayText(),
                                                       int(self.ui.lineEdit_2.displayText()),
                                                       self.ui.lineEdit_3.displayText(),
                                                       self.ui.lineEdit_4.displayText(),
                                                       self.ui.lineEdit_5.displayText(),
                                                       self.ui.lineEdit_6.displayText())
            elif self.ui.radioButton_3.isChecked():
                output = self.read_database_mysql(self.ui.lineEdit.displayText(),
                                                  int(self.ui.lineEdit_2.displayText()),
                                                  self.ui.lineEdit_3.displayText(),
                                                  self.ui.lineEdit_4.displayText(),
                                                  self.ui.lineEdit_5.displayText(),
                                                  self.ui.lineEdit_6.displayText())
            for line in output:
                self.ui.textBrowser.append(line)
            self.ui.textBrowser.scrollToAnchor("scroll")
        except Exception as er:
            self.ui.textBrowser.append(f'{er}')
