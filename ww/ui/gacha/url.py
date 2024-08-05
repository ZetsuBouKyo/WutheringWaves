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

API_URL = "https://gmserver-api.aki-game2.net/gacha/record/query"


class QGachaUrlTab(QWidget):
    def __init__(self, api_url: str = API_URL):
        super().__init__()
        self.api_url = api_url
        self.layout = QVBoxLayout()

        self.q_analyze_layout = QHBoxLayout()
        self.q_url = QLineEdit()
        self.q_url.setFixedHeight(32)
        self.q_analyze_btn = QPushButton("分析")
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_analyze_layout.addWidget(self.q_url, 1)
        self.q_analyze_layout.addWidget(self.q_analyze_btn)

        self.layout.addLayout(self.q_analyze_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def analyze(self):
        url = self.q_url.text()
        parsed_url = urlparse(url, allow_fragments=False)
        parsed_parameters = parse_qs(parsed_url.query)
        parameters = {"cardPoolType": 1}
        keys = {"svr_id", "player_id", "lang", "svr_area", "record_id", "resources_id"}
        for key, value in parsed_parameters.items():
            if key not in keys:
                continue
            parameters[key] = value[0]

        # response = requests.post(
        #     self.api_url,
        #     headers={
        #         "Content-type": "application/json",
        #         "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        #     },
        #     json=parameters,
        # )
        # if response.status_code != 200:
        #     return

        # data = response.json()
        # print(data)
