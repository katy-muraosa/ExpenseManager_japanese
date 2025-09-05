from PySide6.QtWidgets import QApplication
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())