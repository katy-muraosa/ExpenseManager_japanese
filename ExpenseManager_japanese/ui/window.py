from PySide6.QtWidgets import QMainWindow, QTabWidget, QStatusBar,QLabel
from tabs.inputtab import InputTab
from tabs.tabletab import TableTab
from tabs.analysistab import AnalysisTab


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("出費管理アプリケーション")
        self.setGeometry(100, 100, 450, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.input_tab = InputTab(self)
        self.table_tab = TableTab(self)
        self.analysis_tab = AnalysisTab(self)

        self.tabs.addTab(self.input_tab, "出費入力")
        self.tabs.addTab(self.table_tab, "出費一覧")
        self.tabs.addTab(self.analysis_tab, "分析")

        self.statusbar = QStatusBar()
        self.file_name = QLabel("-")
        self.file_path = ""
        self.setStatusBar(self.statusbar)
        self.statusbar.addPermanentWidget(self.file_name)

