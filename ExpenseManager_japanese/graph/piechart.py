from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

matplotlib.rcParams['font.family'] = 'Hiragino Sans'

class PieChart(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(4,3))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def generate_piechart(self, sizes=[100], labels=["No Data"]):
        cmap = matplotlib.cm.get_cmap("tab20")
        colors = cmap(range(len(labels)))
        self.ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors)
        self.ax.set_title("項目別出費割合")
        self.draw()