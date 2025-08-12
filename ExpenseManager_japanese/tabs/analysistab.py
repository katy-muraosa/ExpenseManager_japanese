from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QGroupBox, QSplitter
from PySide6.QtCore import Qt
import pandas as pd
from graph.piechart import PieChart
from collections import Counter


class AnalysisTab(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.layout = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        self.setLayout(self.layout)

        self.label_box = QGroupBox("出費項目一覧")
        self.chart_box = QGroupBox("グラフ")
        self.total_expense_box = QGroupBox("集計と分析")
        
        self.label_layout = QVBoxLayout()
        self.chart_layout = QVBoxLayout()
        self.total_layout = QVBoxLayout()
        

        self.label = QLabel()
        self.label.setTextFormat(Qt.RichText)
        self.label.setText("No Data :0件 ¥0")
        self.label.setWordWrap(True) 

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.label)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(175)

        self.chart = PieChart()
        self.chart.generate_piechart()

        self.total_expense_label = QLabel("総出費額：¥0")

        self.chart_layout.addWidget(self.chart)
        self.label_layout.addWidget(self.scroll)
        self.total_layout.addWidget(self.total_expense_label)

        self.chart_box.setLayout(self.chart_layout)
        self.label_box.setLayout(self.label_layout)
        self.total_expense_box.setLayout(self.total_layout)

        splitter.addWidget(self.label_box)
        splitter.addWidget(self.chart_box)
        splitter.addWidget(self.total_expense_box)

        splitter.setSizes([50, 500, 50])

        self.layout.addWidget(splitter)

        
    def draw_piechart(self):
        data = self.main_window.table_tab.get_data()
        self.df = pd.DataFrame(data, columns=["日付", "出費項目", "金額"])
        self.grouped = self.df.groupby("出費項目")["金額"].sum()
        sum_df = self.grouped.reset_index()
        sum_df.columns = ["出費項目", "合計金額"]

        item_counts = Counter(self.df["出費項目"])
        counts_df = pd.DataFrame.from_dict(item_counts, orient="index").reset_index()
        counts_df.columns = ["出費項目", "件数"]
        self.merge_df  = pd.merge(counts_df, sum_df, on="出費項目").sort_values("合計金額", ascending=False)

        self.labels = self.grouped.index.tolist()
        self.sizes = self.grouped.values.tolist()
        self.merges = self.merge_df.values.tolist()

        self.chart.generate_piechart(self.sizes, self.labels)

    def summary(self, data=[['No Data', 0, 0]]):
        html = ""
        total_expense = 0
        new_data = data
        for category, count, total in new_data:
            html += f'<p><b>{category}</b>：{count}件 (¥{int(total):,})</p>'
            total_expense += total

        self.label.setText(html)
        self.total_expense_label.setText(f'総出費額：¥{int(total_expense):,}')




    def update_graph(self):
        self.chart.ax.clear()
        self.draw_piechart()
        self.summary(self.merges)