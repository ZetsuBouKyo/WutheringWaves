import json
import sys
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


class PoolModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    total: int = 0
    standard_resonator_5: int = 0
    featured_resonator_5: int = 0
    standard_weapon_5: int = 0
    featured_weapon_5: int = 0

    pool_type: Optional[GachaPoolTypeEnum] = None
    resonators: List[Union[str, GachaResonatorModel]] = []
    weapons: List[Union[str, GachaWeaponModel]] = []


def parse(data: dict):
    pool = PoolModel()

    d = data.get("data", [])
    if len(d) == 0:
        return pool
    d = d[0]

    properties = d.get("properties", None)
    if properties is None:
        return pool

    gacha_item_id = properties.get("gacha_item_id", None)
    if gacha_item_id is None:
        return pool

    gacha_item_ids = gacha_item_id.split(",")
    pool.total = len(gacha_item_ids)
    if pool.total < 160:
        return pool

    for id in gacha_item_ids:
        resonator = resonators.get(id, None)
        weapon = weapons.get(id, None)

        if resonator is not None and type(resonator) != str:
            if resonator.rank == 5:
                if resonator.permanent:
                    pool.standard_resonator_5 += 1
                else:
                    pool.featured_resonator_5 += 1
            pool.resonators.append(resonator)
        if weapon is not None and type(weapon) != str:
            if weapon.rank == 5:
                if weapon.permanent:
                    pool.standard_weapon_5 += 1
                else:
                    pool.featured_weapon_5 += 1
            pool.weapons.append(weapon)

    if pool.featured_resonator_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.FEATURED_RESONATOR_CONVENE.value
    elif pool.featured_weapon_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.FEATURED_WEAPON_CONVENE.value
    elif pool.standard_weapon_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.STANDARD_WEAPON_CONVENE.value
    elif pool.standard_resonator_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.STANDARD_RESONATOR_CONVENE.value

    return pool


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
        pool_types = set()
        pools = []
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
                    if pool.pool_type in pool_types:
                        continue
                    pool_types.add(pool.pool_type)
                    pools.append(pool)
        print(pools)
