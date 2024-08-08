import json
import sys
from copy import deepcopy
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict
from PySide2.QtCore import QRect, QSize, Qt
from PySide2.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PySide2.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.crud.resonator import get_resonator_icon_path
from ww.locale import ZhHantEnum, _
from ww.model.pool import GachaPoolTypeEnum
from ww.ui.combobox import QCustomComboBox
from ww.ui.gacha.id_to_name import (
    GachaResonatorModel,
    GachaWeaponModel,
    resonators,
    weapons,
)
from ww.ui.gacha.pool import PoolModel
from ww.ui.layout import FlowLayout
from ww.ui.widget import ScrollableWidget


class QGachaIcon(QWidget):
    def __init__(
        self,
        number: int,
        icon_name: str,
        icon_fpath: Optional[str],
        icon_width: int = 100,
        icon_height: int = 100,
    ):
        super().__init__()

        layout = QVBoxLayout()

        # Icon
        if icon_fpath is None:
            button = QPushButton(icon_name)
        else:
            button = QPushButton()
            button.setIcon(QIcon(icon_fpath))
            button.setIconSize(QSize(icon_width, icon_height))
        button.setToolTip(icon_name)
        button.setFixedSize(QSize(icon_width, icon_height))
        # button.setStyleSheet("")

        # Number
        label_layout = QHBoxLayout()
        label = QLabel(str(number))
        label.setFont(QFont("Arial", 16))
        label_layout.addStretch()
        label_layout.addWidget(label)
        label_layout.addStretch()

        layout.addWidget(button)
        layout.addLayout(label_layout)

        self.setLayout(layout)


def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clearLayout(item.layout())


class QGachaResults(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = FlowLayout()
        self.setLayout(self.layout)

    def set_results(
        self,
        pool_name: GachaPoolTypeEnum,
        pools: Dict[str, PoolModel],
        show_4_star: bool = False,
    ):
        clearLayout(self.layout)

        pool = pools.get(pool_name, None)
        if pool is None:
            return

        for result in pool.results:
            if not show_4_star and result.star <= 4:
                continue

            if not isinstance(result, GachaResonatorModel):
                continue
            icon_path = get_resonator_icon_path(result.name)
            icon = QGachaIcon(result.number, result.name, icon_path)
            self.layout.addWidget(icon)


class QGachaAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Tool bar
        self.q_tool_bar_layout = QHBoxLayout()
        self.q_pool_combobox = QCustomComboBox()
        self.q_pool_combobox.setFixedWidth(200)
        self.q_pool_combobox.setFixedHeight(40)
        self.q_pool_combobox.addItems([e.value for e in GachaPoolTypeEnum])
        self.q_4_start_checkbox = QCheckBox(_(ZhHantEnum.SHOW_4_STAR))
        self.q_tool_bar_layout.addWidget(self.q_pool_combobox)
        self.q_tool_bar_layout.addWidget(self.q_4_start_checkbox)
        self.q_tool_bar_layout.addStretch()

        # Result
        self.q_results = QGachaResults()
        self.q_results_main = ScrollableWidget(self.q_results)

        self.layout.addLayout(self.q_tool_bar_layout)
        self.layout.addWidget(self.q_results_main)

        self.setLayout(self.layout)

    def set_results(self, pools: Dict[str, PoolModel]):
        pool_name = self.q_pool_combobox.currentText()
        self.q_results.set_results(
            pool_name, pools, self.q_4_start_checkbox.isChecked()
        )
