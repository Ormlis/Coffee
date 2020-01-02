import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.show_from_request('Select * from coffee')
        self.edit_find.textChanged.connect(self.find_coffee)

    def show_from_request(self, req):
        self.tableWidget.clear()
        cur = self.con.cursor()
        result = cur.execute(req).fetchall()
        if not result:
            result = cur.execute(f"Select * from coffee").fetchall()

        self.description = cur.description
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in self.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def find_coffee(self):
        coffee = self.edit_find.text()
        self.show_from_request(f"Select * from coffee where variety_name = '{coffee}'")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
