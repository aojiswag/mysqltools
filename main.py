from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
import sys
import os
import shutil
import numpy
import pymysql
import csv
import win32api
import threading

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
UI_PATH = BASE_PATH + "/gui/main.ui"
DEFAULT_DB_FORM_PATH = BASE_PATH + "/config/dbform.csv"


def msg_box(text: str, title: str, utype: int):
    ok = win32api.MessageBox(0, text, title, utype)


def open_with_window(path: str):
    os.system(path)


class MainWindow(QMainWindow, uic.loadUiType(UI_PATH)[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.push_button_create_table_form_and_open.clicked.connect(self.create_table_form_and_open)
        self.push_button_create_table_from_table_form.clicked.connect(self.create_table_from_table_form)
        self.push_button_open_table_form.clicked.connect(self.open_table_form)

    def create_table_form_and_open(self):
        try:
            form_file = QFileDialog.getSaveFileName(self, 'Add form', BASE_PATH,
                                                    "Comma Separated Values (*.csv)")
            shutil.copy(DEFAULT_DB_FORM_PATH, form_file[0])
            self.line_edit_table_form_dir.setText(form_file[0])

            file_edit_thread = threading.Thread(target=open_with_window, args=(form_file[0],))
            file_edit_thread.start()

        except FileNotFoundError:
            return

    def create_table_from_table_form(self):
        try:
            connection = pymysql.connect(host="127.0.0.1", user="root", password=self.line_edit_password.text(),
                                         db=self.line_edit_db_name.text(), charset='utf8')
        except pymysql.err.OperationalError:
            msg_box("Dbname or password error", "error", 0)

            return

        db = connection.cursor()
        with open(self.line_edit_table_form_dir.text(), newline='') as table_form_file:
            reader = csv.reader(table_form_file)
            data = list(reader)

        sql = "CREATE TABLE " + self.line_edit_table_name.text() + "("

        for i in range(1, len(data), 1):
            if data[i][0] != "" and data[i][1] != "" and data[i][2] != "":
                if i == len(data) - 1:
                    sql = sql + "{0} {1}({2}))".format(data[i][0], data[i][1], data[i][2])
                else:
                    sql = sql + "{0} {1}({2}),".format(data[i][0], data[i][1], data[i][2])

        print(sql)
        db.execute(sql)

        connection.close()

    def open_table_form(self):
        try:
            form_file = QFileDialog.getOpenFileName(self, 'Add form', BASE_PATH,
                                                    "Comma Separated Values (*.csv)")
            self.line_edit_table_form_dir.setText(form_file[0])
        except FileNotFoundError:
            return

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # update font size when resized (dynamic)
        resize_parent = self.findChildren(QGridLayout, name="grid_layout_insert_table_tool")[0]
        for i in range(resize_parent.count()):
            widget = resize_parent.itemAt(i).widget()
            if widget is not None:
                font = widget.font()
                font.setPointSize(int(widget.geometry().height() / 3) - 2)
                widget.setFont(font)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MainWindow()
    myApp.show()
    sys.exit(app.exec_())
