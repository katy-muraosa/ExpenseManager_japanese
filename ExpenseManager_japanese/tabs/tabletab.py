from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton


class TableTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["日付", "出費項目", "金額", "メモ"])
        self.layout.addWidget(self.table)

        self.delete_button = QPushButton("行を削除")
        self.delete_button.clicked.connect(self.delete_selected_row)
        self.layout.addWidget(self.delete_button)

    def delete_selected_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
        self.main_window.analysis_tab.update_graph()

    def create_item(self, value):
        return QTableWidgetItem(str(value))
    
    def get_data(self):
        self.data = []
        for row in range(self.table.rowCount()):
            row_data = {
                "日付":self.table.item(row, 0).text(),
                "出費項目":self.table.item(row, 1).text(),
                "金額":int(self.table.item(row, 2).text().translate(str.maketrans({',':''}))),
                "メモ":self.table.item(row, 3).text()
            }
            self.data.append(row_data)
        return self.data
    
    def load_data(self, data):
        self.table.setRowCount(0)
        for i, row_data in enumerate(data):
            self.table.insertRow(i)
            for col, key in enumerate(["日付", "出費項目", "金額", "メモ"]):
                if col == 2:
                    self.table.setItem(i, col, self.create_item('{0:,}'.format(int(row_data[key]))))
                else:
                    self.table.setItem(i, col, self.create_item(row_data[key]))