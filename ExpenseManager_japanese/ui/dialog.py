from PySide6.QtWidgets import QFileDialog, QMessageBox
from storage.storage import save_json, load_json
import os

def get_document_path(self):
    try:
        file_path, filtr = QFileDialog.getOpenFileName(
            parent=self,
            caption="ファイルを読み込む",
            filter="jsonファイル (*.json);;すべてのファイル(*.*)"
        )
        if not file_path:
            return

        data = load_json(file_path)
        self.main_window.table_tab.load_data(data)
        self.main_window.input_tab.temporary_message("読み込みは完了しました")

        self.main_window.file_name.clear()
        self.main_window.file_name.setText(os.path.basename(file_path))
        self.main_window.file_path = file_path
        self.main_window.analysis_tab.update_graph()
        
    except Exception:
        QMessageBox.critical(self, "読み込みエラー", "ファイルは読み込めていません")

def save_document_path(self):
    try:
        file_path, filtr = QFileDialog.getSaveFileName(
            parent=self,
            caption="ファイルを保存",
            filter="jsonファイル(*.json)"
        )
        if not file_path:
            return

        data = self.main_window.table_tab.get_data()
        

        save_json(data, file_path)
        self.main_window.input_tab.temporary_message("保存は完了しました")

        self.main_window.file_name.clear()
        self.main_window.file_name.setText(os.path.basename(file_path))
        self.main_window.file_path = file_path
        self.main_window.analysis_tab.update_graph()
        
    except Exception:
        QMessageBox.critical(self, "保存エラー", "保存は完了していません")