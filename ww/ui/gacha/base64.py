import base64
import sys
from functools import partial
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class QGachaBase64Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_analyze_layout = QHBoxLayout()
        self.q_base64 = QLineEdit()
        self.q_base64.setFixedHeight(32)
        self.q_analyze_btn = QPushButton("分析")
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_analyze_layout.addWidget(self.q_base64, 1)
        self.q_analyze_layout.addWidget(self.q_analyze_btn)

        self.layout.addLayout(self.q_analyze_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def analyze(self):
        str_base64 = self.q_base64.text()
        data = base64.b64decode(str_base64).decode("utf-8")
        print(data)
