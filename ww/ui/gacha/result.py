from decimal import Decimal
from typing import Dict, Optional

from PySide2.QtCore import QSize
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.crud.docs import get_gacha_file_html
from ww.crud.resonator import get_resonator_icon_path
from ww.locale import ZhHantEnum, _
from ww.model.pool import GachaPoolTypeEnum
from ww.ui.combobox import QCustomComboBox
from ww.ui.docs import get_docs
from ww.ui.gacha.id_to_name import GachaResonatorModel
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


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())


class QGachaResults(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.flow_layout = FlowLayout()
        self.layout.addLayout(self.flow_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def clear_results(self):
        clear_layout(self.flow_layout)

    def set_results(self, pool: Optional[PoolModel], show_4_star: bool = False):
        if pool is None:
            return

        for result in pool.results:
            if not show_4_star and result.star <= 4:
                continue

            if not isinstance(result, GachaResonatorModel):
                continue
            icon_path = get_resonator_icon_path(result.name)
            icon = QGachaIcon(result.number, result.name, icon_path)
            self.flow_layout.addWidget(icon)


class QGachaResultTab(QWidget):
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

        self.init_analysis()

        # Result
        self.q_results = QGachaResults()
        self.q_results_main = ScrollableWidget(self.q_results)

        self.layout.addLayout(self.q_tool_bar_layout)
        self.layout.addWidget(self.q_results_main)

        self.setLayout(self.layout)

    def set_label(self, title: str) -> QLabel:
        layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setFixedWidth(150)
        title_label.setFixedHeight(40)
        value_label = QLabel("")
        value_label.setFixedHeight(40)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        self.layout.addLayout(layout)
        return value_label

    def init_analysis(self):
        self.q_total_pulls_label = self.set_label(f"{_(ZhHantEnum.TOTAL_PULLS)}:")
        self.q_total_5_star_pulls_label = self.set_label(
            f"{_(ZhHantEnum.TOTAL_5_STAR_PULLS)}:"
        )
        self.q_remained_5_star_pulls_label = self.set_label(
            f"{_(ZhHantEnum.REMAINED_5_STAR_PULLS)}:"
        )
        self.q_remained_4_star_pulls_label = self.set_label(
            f"{_(ZhHantEnum.REMAINED_4_STAR_ABOVE_PULLS)}:"
        )
        self.q_from_old_to_new_label = self.set_label(
            f"{_(ZhHantEnum.FROM_OLD_TO_NEW)}:"
        )

    def clear_analysis(self):
        self.q_total_pulls_label.setText("")
        self.q_total_5_star_pulls_label.setText("")
        self.q_remained_5_star_pulls_label.setText("")
        self.q_remained_4_star_pulls_label.setText("")

    def set_analysis(self, pool: PoolModel):
        self.q_total_pulls_label.setText(str(pool.total))

        pulls_5_star = (
            pool.featured_resonator_5
            + pool.featured_weapon_5
            + pool.standard_resonator_5
            + pool.standard_weapon_5
        )
        pulls_5_star_rate = Decimal(pulls_5_star) / Decimal(pool.total)
        pulls_5_star_str = f"{pulls_5_star} ({pulls_5_star_rate:.2%})"
        self.q_total_5_star_pulls_label.setText(pulls_5_star_str)

        self.q_remained_5_star_pulls_label.setText(str(pool.remainder_5))
        self.q_remained_4_star_pulls_label.setText(str(pool.remainder_4_or_5))

    def set_results(self, pools: Dict[str, PoolModel]):
        pool_name = self.q_pool_combobox.currentText()
        pool_name = pool_name.strip()

        self.clear_analysis()
        self.q_results.clear_results()

        if pool_name == "":
            QMessageBox.warning(
                self, _(ZhHantEnum.WARNING), _(ZhHantEnum.POOL_NAME_MUST_NOT_EMPTY)
            )
            return

        pool = pools.get(pool_name, None)
        if pool is None:
            QMessageBox.warning(
                self, _(ZhHantEnum.WARNING), _(ZhHantEnum.POOL_NAME_NOT_LEGAL)
            )
            return

        self.set_analysis(pool)
        self.q_results.set_results(pool, self.q_4_start_checkbox.isChecked())


class QGachaResultsTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_gacha_result_tab = QGachaResultTab()
        self.q_gacha_help_tab = get_docs(get_gacha_file_html)

        self.addTab(self.q_gacha_result_tab, _(ZhHantEnum.TAB_ANALYSIS))
        self.addTab(self.q_gacha_help_tab, _(ZhHantEnum.TAB_HELP))

    def set_results(self, pools: Dict[str, PoolModel]):
        self.q_gacha_result_tab.set_results(pools)
