import sys
from functools import partial
from pathlib import Path

from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class QGachaFileTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_browse_btn = QPushButton("選擇檔案")
        self.q_browse_btn.clicked.connect(self.open_file_dialog)
        self.q_btns_layout.addWidget(self.q_browse_btn)
        self.q_btns_layout.addStretch()

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def open_file_dialog(self):
        q_file_dialog = QFileDialog(self)
        fpath, _ = q_file_dialog.getOpenFileName(
            self, "開啟檔案", "", "All Files (*);;Text Files (*.txt)"
        )
        if not fpath:
            return
        print(f"Selected file: {fpath}")
        fpath = Path(fpath)
        if not fpath.exists():
            return

        lines = []
        with fpath.open(mode="r", encoding="utf-8") as fp:
            for line in fp.readlines():
                lines.append(line)
