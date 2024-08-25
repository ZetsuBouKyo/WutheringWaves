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
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.locale import ZhTwEnum, _
from ww.model.pool import GachaPoolTypeEnum
from ww.model.pool.id_to_name import (
    GachaResonatorModel,
    GachaWeaponModel,
    resonators,
    weapons,
)
from ww.ui.gacha.pool import parse
from ww.ui.gacha.result import QGachaResultsTabs


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

        self.q_gacha_analysis = QGachaResultsTabs()

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_gacha_analysis, 1)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def set_fpath(self, fpath: Optional[Path]):
        self.fpath = fpath
        fpath_str = ""
        if self.fpath is not None:
            fpath_str = str(self.fpath)
        self.q_fpath_label.setText(fpath_str)

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
        self.set_fpath(fpath)

    def analyze(self):
        if self.fpath is None:
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                _(ZhTwEnum.WUTHERING_WAVES_DEBUG_FILE_NOT_FOUND),
            )
            return

        if self.fpath.parts[-2] == "KRSDKWebView":
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                _(ZhTwEnum.WUTHERING_WAVES_DEBUG_FILE_SHOULD_BE_COPIED),
            )
            self.set_fpath(None)
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

        self.q_gacha_analysis.set_results(pools)
