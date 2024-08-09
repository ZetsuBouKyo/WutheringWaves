from PySide2.QtWidgets import (
    QApplication,
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

from ww.crud.weapon import get_weapon_names
from ww.locale import ZhHantEnum, _
from ww.model.weapon import WeaponPassiveStatEnum, WeaponRankEnum, WeaponStatEnum
from ww.tables.weapon import get_weapon_rank_fpath, get_weapon_stat_fpath
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.utils.pd import get_empty_df


class QPrivateDataWeaponStatTable(QDraggableTableWidget):
    def __init__(self):
        column_names = [WeaponStatEnum.LEVEL.value, WeaponStatEnum.ATK.value, ""]
        df = get_empty_df(column_names)
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=WeaponStatEnum.LEVEL.value,
            column_names=column_names,
        )


class QPrivateDataWeaponStatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataWeaponStatTable()
        self.q_tsv = QDraggableTsvTableWidget(self.q_table)
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)

    def load(self, weapon_name: str):
        tsv_fpath = get_weapon_stat_fpath(weapon_name)
        if tsv_fpath is None:
            return

        self.q_tsv.set_tsv_fpath(tsv_fpath)
        self.q_tsv.load()


class QPrivateDataWeaponTuneTable(QDraggableTableWidget):
    def __init__(self):
        column_names = [WeaponRankEnum.LEVEL.value, ""]
        df = get_empty_df(column_names)
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=WeaponRankEnum.LEVEL.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 400)


class QPrivateDataWeaponTuneTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        q_passive_stat_combobox_columns = [e.value for e in WeaponPassiveStatEnum]

        self.q_passive_stat_layout = QHBoxLayout()
        self.q_passive_stat_label = QLabel(_(ZhHantEnum.WEAPON_PASSIVE_STAT))
        self.q_passive_stat_label.setFixedHeight(40)
        self.q_passive_stat_combobox = QCustomComboBox()
        self.q_passive_stat_combobox.addItems(q_passive_stat_combobox_columns)
        self.q_passive_stat_combobox.setFixedHeight(40)
        self.q_passive_stat_combobox.setFixedWidth(300)
        self.q_passive_stat_combobox.currentIndexChanged.connect(self.set_passive_stat)
        self.q_passive_stat_layout.addWidget(self.q_passive_stat_label)
        self.q_passive_stat_layout.addWidget(self.q_passive_stat_combobox)
        self.q_passive_stat_layout.addStretch()
        self.layout.addLayout(self.q_passive_stat_layout)

        self.q_table = QPrivateDataWeaponTuneTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, event_load_after=self.load_passive_stat
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)

    def set_passive_stat(self):
        column_names = self.q_tsv.get_column_names()
        column_names[-1] = self.q_passive_stat_combobox.currentText()
        self.q_tsv.set_column_names(column_names)

    def load_passive_stat(self):
        column_names = self.q_tsv.get_column_names()
        passive_stat = column_names[-1]
        self.q_passive_stat_combobox.setCurrentText(passive_stat)

    def load(self, weapon_name: str):
        tsv_fpath = get_weapon_rank_fpath(weapon_name)
        if tsv_fpath is None:
            return

        self.q_tsv.set_tsv_fpath(tsv_fpath)
        self.q_tsv.load()
        self.load_passive_stat()


class QPrivateDataWeaponTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.q_weapon_layout = QHBoxLayout()
        self.q_weapon_label = QLabel(_(ZhHantEnum.NAME))
        self.q_weapon_label.setFixedHeight(40)
        self.q_weapon_combobox = QCustomComboBox(getOptions=get_weapon_names)
        self.q_weapon_combobox.setFixedHeight(40)
        self.q_weapon_combobox.setFixedWidth(150)
        self.q_weapon_combobox.currentIndexChanged.connect(self.load_tabs)

        self.q_weapon_layout.addWidget(self.q_weapon_label)
        self.q_weapon_layout.addWidget(self.q_weapon_combobox)
        self.q_weapon_layout.addStretch()

        # Tabs
        self.q_tabs = QTabWidget()
        self.q_stat_tab = QPrivateDataWeaponStatTab()
        self.q_tune_tab = QPrivateDataWeaponTuneTab()

        self.q_tabs.addTab(self.q_stat_tab, _(ZhHantEnum.TAB_STAT))
        self.q_tabs.addTab(self.q_tune_tab, _(ZhHantEnum.TAB_TUNE))

        self.layout.addLayout(self.q_weapon_layout)
        self.layout.addWidget(self.q_tabs)

        self.setLayout(self.layout)

    def load_tabs(self):
        weapon_name = self.q_weapon_combobox.currentText()
        if not weapon_name:
            return

        self.q_stat_tab.load(weapon_name)
        self.q_tune_tab.load(weapon_name)
