from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
import sys
import os
import shutil

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
UI_PATH = BASE_PATH + "/gui/main.ui"
DEFAULT_DB_FORM_PATH = BASE_PATH + "/config/dbform.csv"


class MainWindow(QMainWindow, uic.loadUiType(UI_PATH)[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.push_button_create_table_form_and_open.clicked.connect(self.create_table_form_and_open)
        self.push_button_insert_table_from_table_form.clicked.connect(self.insert_table_from_table_form)
        self.push_button_open_table_form.clicked.connect(self.open_table_form)

    def create_table_form_and_open(self):
        form_file = QFileDialog.getSaveFileName(self, 'Add form', BASE_PATH,
                                                "Comma Separated Values (*.csv)")
        shutil.copy(DEFAULT_DB_FORM_PATH, form_file[0])
        self.line_edit_table_form_dir.setText(form_file[0])

    def insert_table_from_table_form(self):
        pass

    def open_table_form(self):
        form_file = QFileDialog.getOpenFileName(self, 'Add form', BASE_PATH,
                                                "Comma Separated Values (*.csv)")
        self.line_edit_table_form_dir.setText(form_file[0])


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # update font size when resized (dynamic)
        resize_parent = self.findChildren(QGridLayout, name="grid_layout_insert_table_tool")[0]

        for i in range(resize_parent.count()):
            widget = resize_parent.itemAt(i).widget()
            if widget is not None:
                font = widget.font()
                font.setPointSize(int(widget.geometry().height() / 2) - 2)
                widget.setFont(font)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MainWindow()
    myApp.show()
    sys.exit(app.exec_())
