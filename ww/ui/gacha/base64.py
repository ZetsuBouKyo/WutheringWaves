import base64
import json
from typing import List

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ww.model.pool import PoolModel
from ww.ui.gacha.pool import get_pool_by_ids
from ww.ui.gacha.result import QGachaResultsTabs


class QGachaBase64Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_analyze_layout = QHBoxLayout()
        self.q_analyze_btn = QPushButton("分析")
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_analyze_layout.addStretch()
        self.q_analyze_layout.addWidget(self.q_analyze_btn)

        self.q_base64_layout = QHBoxLayout()
        self.q_base64_label = QLabel("Base64")
        self.q_base64_label.setFixedWidth(150)
        self.q_base64_label.setFixedHeight(32)
        self.q_base64 = QLineEdit()
        self.q_base64.setFixedHeight(32)
        self.q_base64_layout.addWidget(self.q_base64_label, 1)
        self.q_base64_layout.addWidget(self.q_base64, 1)

        self.q_list_layout = QHBoxLayout()
        self.q_list_label = QLabel("IDs")
        self.q_list_label.setFixedWidth(150)
        self.q_list_label.setFixedHeight(32)
        self.q_list = QLineEdit()
        self.q_list.setFixedHeight(32)
        self.q_list_layout.addWidget(self.q_list_label, 1)
        self.q_list_layout.addWidget(self.q_list, 1)

        self.q_gacha_analysis = QGachaResultsTabs()

        self.layout.addLayout(self.q_analyze_layout)
        self.layout.addLayout(self.q_base64_layout)
        self.layout.addLayout(self.q_list_layout)
        self.layout.addWidget(self.q_gacha_analysis, 1)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def analyze(self):
        str_base64 = self.q_base64.text()
        ids_str = self.q_list.text()
        if str_base64:
            data_str = base64.b64decode(str_base64).decode("utf-8")
            print(data_str)

            data = json.loads(data_str)
            ids_str = (
                data.get("data", [None])[0]
                .get("properties", {})
                .get("gacha_item_id", None)
            )

        if not ids_str:
            return

        ids: List[str] = ids_str.split(",")
        ids = ids[::-1]
        pool = PoolModel()
        pool = get_pool_by_ids(ids, pool=pool)
        pools = {pool.pool_type: pool}
        self.q_gacha_analysis.set_results(pools)
