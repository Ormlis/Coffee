import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.show_from_request('Select * from coffee')
        self.edit_find.textChanged.connect(self.find_coffee)
        self.pushButton.clicked.connect(self.open_add_edit)

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

    def open_add_edit(self):
        self.add_edit_wind = AddEdit(self.titles)
        self.add_edit_wind.exec()
        self.show_from_request(f"Select * from coffee")


class AddEdit(QDialog):
    def __init__(self, titles):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.tableWidget.setColumnCount(len(titles))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(1)
        self.lineEdit.textChanged.connect(self.find)
        self.pushButton.clicked.connect(self.save)
        self.id = None

    def find(self):
        for j in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(0, j, QTableWidgetItem(''))
        cur = self.con.cursor()
        result = None
        if self.lineEdit.text().isdigit():
            result = cur.execute(
                f'Select * from coffee where id = {self.lineEdit.text()}').fetchall()
        if not result:
            self.id = None
            return

        self.id = int(self.lineEdit.text())
        for j, val in enumerate(result[0]):
            self.tableWidget.setItem(0, j, QTableWidgetItem(str(val)))

    def save(self):
        values = []
        for i in range(self.tableWidget.columnCount()):
            values.append(self.tableWidget.item(0, i).text())

        values = list(map(lambda x: x if x.isdigit() else f"'{x}'", values))

        cur = self.con.cursor()
        if self.id is None:
            cur.execute(f"INSERT INTO coffee VALUES({', '.join(values)})")
        else:
            for i in range(len(values)):
                values[i] = self.tableWidget.horizontalHeaderItem(i).text() + ' = ' + values[i]
            cur.execute(f"UPDATE coffee SET {', '.join(values)} WHERE id = {self.id}")
        self.con.commit()
        self.close()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
