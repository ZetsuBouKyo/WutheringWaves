import json
import sys
from copy import deepcopy
from enum import Enum
from functools import partial
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict
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

from ww.model.pool import GachaPoolTypeEnum
from ww.ui.gacha.id_to_name import (
    GachaResonatorModel,
    GachaWeaponModel,
    resonators,
    weapons,
)
from ww.ui.gacha.pool import parse
from ww.ui.gacha.result import QGachaAnalysis


class QGachaFileTab(QWidget):
    def __init__(self):
        self.fpath: Optional[Path] = None

        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_browse_btn = QPushButton("選擇檔案")
        self.q_browse_btn.clicked.connect(self.open_file_dialog)
        self.q_fpath_label = QLabel("")
        self.q_analyze_btn = QPushButton("分析")
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_btns_layout.addWidget(self.q_browse_btn)
        self.q_btns_layout.addWidget(self.q_fpath_label)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_analyze_btn)

        self.q_gacha_analysis = QGachaAnalysis()

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_gacha_analysis, 1)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def open_file_dialog(self):
        q_file_dialog = QFileDialog(self)
        fpath, _ = q_file_dialog.getOpenFileName(
            self, "開啟檔案", "", "All Files (*);;Text Files (*.txt)"
        )
        if not fpath:
            return

        fpath = Path(fpath)
        if not fpath.exists():
            return
        self.fpath = fpath
        self.q_fpath_label.setText(str(self.fpath))

    def analyze(self):
        if self.fpath is None:
            return

        with self.fpath.open(mode="r", encoding="utf-8") as fp:
            raw_data = fp.read()
            lines = raw_data.split("\n")

        start = -1
        end = -1

        pools = {}
        for i in range(-1, -1 - len(lines), -1):
            if lines[i].startswith('}",'):
                end = i
            elif lines[i].endswith('"{'):
                start = i
            if start < end:
                data = ["{"] + lines[start + 1 : end] + ["}"]
                data = "".join(data)
                data = json.loads(data)

                pool = parse(data)
                if pool.pool_type is not None:
                    if pool.pool_type in pools:
                        continue
                    pools[pool.pool_type] = pool

        for _, pool in pools.items():
            print(pool.model_dump_json(indent=4))

        self.q_gacha_analysis.set_results(pools)
