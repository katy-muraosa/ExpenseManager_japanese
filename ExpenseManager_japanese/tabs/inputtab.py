from PySide6.QtWidgets import (
    QWidget, QCalendarWidget, QVBoxLayout, 
    QPushButton, QRadioButton, QLineEdit, QGroupBox, 
    QLabel, QGridLayout, QMessageBox
)
from PySide6.QtGui import QIntValidator
from ui.dialog import get_document_path, save_document_path
from ui.confirmdialog import ConfirmDialog
from storage.storage import save_json
from functools import partial






class InputTab(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.calendarbox = QGroupBox("日付選択")
        self.paymentitembox = QGroupBox("出費項目")
        self.moneybox = QGroupBox("金額")
        self.saveandloadbox = QGroupBox("保存と読み込み")
        self.memobox = QGroupBox("メモ")


        self.calendar = QCalendarWidget()
        
        self.life_foodcost = QRadioButton("食費")
        self.life_foodcost.setChecked(True)
        self.life_consumables = QRadioButton("生活消耗品費")
        self.life_rent = QRadioButton("家賃")
        self.life_gas = QRadioButton("ガス")
        self.life_utility = QRadioButton("電気")
        self.life_health = QRadioButton("健康維持費")
        self.other_learning = QRadioButton("勉学費")
        self.other_subscribe = QRadioButton("月購読費")
        self.other_stuck = QRadioButton("投資")
        self.other_otherradio = QRadioButton("その他")
        self.other_otherinput = QLineEdit()
        self.other_otherinput.setPlaceholderText("その他の場合入力してください")
        self.other_otherinput.setEnabled(False)
        self.other_otherradio.toggled.connect(self.other_enabled)

        self.moneyline = QLineEdit()
        self.moneyline.setPlaceholderText("半角数字のみ入力できます")
        self.validator = QIntValidator(0, 9999999)
        self.moneyline.setValidator(self.validator)
        self.money = QLabel("円")

        self.memo = QLineEdit()


        self.enterbutton = QPushButton("表へ入力")
        self.enterbutton.setShortcut("Return")
        self.enterbutton.clicked.connect(self.input_table)

        self.savebutton = QPushButton("新しく保存")
        self.updatesavebutton = QPushButton("上書き保存")
        self.save_document_path = partial(save_document_path, self)
        self.savebutton.clicked.connect(self.save_document_path) 
        self.updatesavebutton.clicked.connect(self.update_save)
        

        self.loadbutton = QPushButton("読み込み")
        self.get_document_path = partial(get_document_path, self)
        self.loadbutton.clicked.connect(self.get_document_path)

        self.all_resetbutton = QPushButton("入力項目のリセット")
        self.all_resetbutton.clicked.connect(self.table_all_reset)

        self.calendarlayout = QVBoxLayout()
        self.calendarlayout.addWidget(self.calendar)
        self.calendarbox.setLayout(self.calendarlayout)

        self.itemlayout = QGridLayout()
        self.itemlayout.addWidget(self.life_foodcost, 0, 0)
        self.itemlayout.addWidget(self.life_consumables, 0, 1)
        self.itemlayout.addWidget(self.life_rent, 0, 2)
        self.itemlayout.addWidget(self.life_gas, 1, 0)
        self.itemlayout.addWidget(self.life_utility, 1, 1)
        self.itemlayout.addWidget(self.life_health, 1, 2)
        self.itemlayout.addWidget(self.other_learning, 2, 0)
        self.itemlayout.addWidget(self.other_subscribe, 2, 1)
        self.itemlayout.addWidget(self.other_stuck, 2, 2)
        self.itemlayout.addWidget(self.other_otherradio, 3, 0)
        self.itemlayout.addWidget(self.other_otherinput, 3, 1, 1, 2)
        self.paymentitembox.setLayout(self.itemlayout)

        self.moneylayout = QGridLayout()
        self.moneylayout.addWidget(self.moneyline, 0, 0)
        self.moneylayout.addWidget(self.money, 0, 1)
        self.moneybox.setLayout(self.moneylayout)

        self.memolayout = QVBoxLayout()
        self.memolayout.addWidget(self.memo)
        self.memobox.setLayout(self.memolayout)

        self.saveloadlayout = QGridLayout()
        self.saveloadlayout.addWidget(self.savebutton, 0, 0)
        self.saveloadlayout.addWidget(self.updatesavebutton, 1, 0)
        self.saveloadlayout.addWidget(self.loadbutton, 0, 1)
        self.saveloadlayout.addWidget(self.all_resetbutton, 1, 1)
        self.saveandloadbox.setLayout(self.saveloadlayout)

    
        self.layout.addWidget(self.calendarbox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.paymentitembox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.moneybox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.memobox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.enterbutton)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.saveandloadbox)

    def other_enabled(self):
        self.other_otherinput.setEnabled(self.other_otherradio.isChecked())

    def temporary_message(self, message):
        self.oneshot_message = self.main_window.statusBar().showMessage(message, 2000)

    def selected_paymentitem(self, groupbox):
        for child in groupbox.findChildren(QRadioButton):
            if child.isChecked():
                return child.text()

    def input_table(self):
        try:
            table = self.main_window.table_tab.table

            text = self.moneyline.text().strip()
            if not text.isdigit():
                self.temporary_message("金額を正しく入力してください")
                return  
           
            self.row = table.rowCount()
            table.insertRow(self.row)
            self.checkitem = self.selected_paymentitem(self.paymentitembox)
        
            self.value = int(text)
        
            table.setItem(self.row, 0, self.main_window.table_tab.create_item(self.calendar.selectedDate().toString("yyyy-MM-dd")))

            if self.checkitem == "その他":
                table.setItem(self.row, 1, self.main_window.table_tab.create_item(self.other_otherinput.text() if self.other_otherinput.text() else "未設定"))
            else:
                table.setItem(self.row, 1, self.main_window.table_tab.create_item(self.checkitem))

            table.setItem(self.row, 2, self.main_window.table_tab.create_item('{0:,}'.format(self.value)))
            table.setItem(self.row, 3, self.main_window.table_tab.create_item(self.memo.text()))

            self.main_window.analysis_tab.update_graph()
            self.temporary_message(f"入力が完了しました：{table.rowCount()}件")

            self.moneyline.clear()
            self.memo.clear()
        except Exception:
            print(self.row)    

    def update_save(self):
        if self.main_window.file_name.text() == "-":
            QMessageBox.critical(self, "上書き保存エラー", "上書き保存するファイルがありません \n新しいファイルとして保存してください")
            self.temporary_message("上書き保存エラー")
        else:
            dialog = ConfirmDialog("上書き保存の確認", "本当に上書き保存しますか？", self)
            dialog.exec()

            if dialog.result() == 1:
                self.data = self.main_window.table_tab.get_data()
                self.file_path = self.main_window.file_path

                save_json(self.data, self.file_path)
                self.temporary_message("上書き保存しました")

            else:
                self.temporary_message("上書き保存を中断しました")

    def table_all_reset(self):
        dialog = ConfirmDialog("入力項目を全てリセット", "表の入力内容を全てリセットしますか？", self)
        dialog.exec()

        if dialog.result() == 1:
            self.main_window.table_tab.table.clearContents()
            self.main_window.table_tab.table.setRowCount(0)
            self.main_window.file_name.setText("-")
            self.main_window.file_path = ""
            self.temporary_message("入力項目がリセットされました")

        else:
            self.temporary_message("入力項目のリセットが中断されました")