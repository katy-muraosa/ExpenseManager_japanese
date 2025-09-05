from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ConfirmDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(300, 175)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))

        ok_button = QPushButton("はい")
        cancel_button = QPushButton("キャンセル")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)
        self.setLayout(layout)