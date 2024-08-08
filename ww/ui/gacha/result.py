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
from ww.model.pool import GachaPoolTypeEnum
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
        icon_fpath: str,
        icon_width: int = 100,
        icon_height: int = 100,
    ):
        super().__init__()

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a button with an icon
        button = QPushButton()
        button.setStyleSheet("")
        button.setIcon(QIcon(icon_fpath))  # Replace with your icon path
        button.setIconSize(
            QSize(icon_width, icon_height)
        )  # Adjust icon size if necessary

        # Create a label for the text
        label_layout = QHBoxLayout()
        label = QLabel(str(number))
        label.setFont(QFont("Arial", 16))
        label_layout.addStretch()
        label_layout.addWidget(label)
        label_layout.addStretch()

        # Add the button and label to the layout
        layout.addWidget(button)
        layout.addLayout(label_layout)

        # Set the layout to the QWidget
        self.setLayout(layout)


class QGachaResults(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = FlowLayout()
        self.setLayout(self.layout)

    def set_results(self, pools: Dict[str, PoolModel]):
        self.layout.itemList = []
        for e_pool_name in GachaPoolTypeEnum:
            pool_name = e_pool_name.value
            pool = pools.get(pool_name, None)
            if pool is None:
                continue
            # results = pool.resonators + pool.weapons
            results = pool.resonators
            for result in results:
                if not isinstance(result, GachaResonatorModel):
                    continue
                icon_path = get_resonator_icon_path(result.name)
                if icon_path is None:
                    continue

                icon = QGachaIcon(result.number, icon_path)
                self.layout.addWidget(icon)


class QGachaAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Result
        self.q_results = QGachaResults()
        self.q_results_main = ScrollableWidget(self.q_results)

        self.layout.addWidget(self.q_results_main)

        self.setLayout(self.layout)

    def set_results(self, pools: Dict[str, PoolModel]):
        self.q_results.set_results(pools)
