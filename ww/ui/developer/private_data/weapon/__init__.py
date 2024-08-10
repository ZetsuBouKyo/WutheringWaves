from PySide2.QtWidgets import (
    QApplication,
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

from ww.crud.weapon import get_weapon_names
from ww.locale import ZhTwEnum, _
from ww.model.weapon import (
    WeaponPassiveStatEnum,
    WeaponRankEnum,
    WeaponStatEnum,
    WeaponSubStatEnum,
)
from ww.tables.weapon import (
    get_weapon_dir_path,
    get_weapon_rank_fpath,
    get_weapon_stat_fpath,
)
from ww.ui.combobox import QAutoCompleteComboBox
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

        q_sub_stat_combobox_columns = [e.value for e in WeaponSubStatEnum]
        self.q_sub_stat_layout = QHBoxLayout()
        self.q_sub_stat_label = QLabel(_(ZhTwEnum.WEAPON_SUB_STAT))
        self.q_sub_stat_label.setFixedHeight(40)
        self.q_sub_stat_label.setFixedWidth(150)
        self.q_sub_stat_combobox = QAutoCompleteComboBox()
        self.q_sub_stat_combobox.addItems(q_sub_stat_combobox_columns)
        self.q_sub_stat_combobox.setFixedHeight(40)
        self.q_sub_stat_combobox.setFixedWidth(300)
        self.q_sub_stat_combobox.currentIndexChanged.connect(self.set_sub_stat)
        self.q_sub_stat_layout.addWidget(self.q_sub_stat_label)
        self.q_sub_stat_layout.addWidget(self.q_sub_stat_combobox)
        self.q_sub_stat_layout.addStretch()
        self.layout.addLayout(self.q_sub_stat_layout)

        self.q_table = QPrivateDataWeaponStatTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, event_load_after=self.load_sub_stat
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)

    def set_sub_stat(self):
        column_names = self.q_tsv.get_column_names()
        column_names[-1] = self.q_sub_stat_combobox.currentText()
        self.q_tsv.set_column_names(column_names)

    def load_sub_stat(self):
        column_names = self.q_tsv.get_column_names()
        sub_stat = column_names[-1]
        self.q_sub_stat_combobox.setCurrentText(sub_stat)

    def load(self, weapon_name: str):
        tsv_fpath = get_weapon_stat_fpath(weapon_name)
        if tsv_fpath is None:
            return

        self.q_tsv.set_tsv_fpath(tsv_fpath)
        self.q_tsv.load(is_confirmation=False)
        self.load_sub_stat()


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
        self.q_passive_stat_label = QLabel(_(ZhTwEnum.WEAPON_PASSIVE_STAT))
        self.q_passive_stat_label.setFixedHeight(40)
        self.q_passive_stat_label.setFixedWidth(150)
        self.q_passive_stat_combobox = QAutoCompleteComboBox()
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
        self.q_tsv.load(is_confirmation=False)
        self.load_passive_stat()


class QPrivateDataWeaponTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.q_weapon_layout = QHBoxLayout()
        self.q_weapon_label = QLabel(_(ZhTwEnum.NAME))
        self.q_weapon_label.setFixedHeight(40)
        self.q_weapon_combobox = QAutoCompleteComboBox(getOptions=get_weapon_names)
        self.q_weapon_combobox.setFixedHeight(40)
        self.q_weapon_combobox.setFixedWidth(150)
        self.q_weapon_combobox.currentTextChanged.connect(self.load_tabs)
        self.q_delete_btn = QPushButton(_(ZhTwEnum.DELETE))
        self.q_delete_btn.clicked.connect(self.delete)

        self.q_weapon_layout.addWidget(self.q_weapon_label)
        self.q_weapon_layout.addWidget(self.q_weapon_combobox)
        self.q_weapon_layout.addStretch()
        self.q_weapon_layout.addWidget(self.q_delete_btn)

        # Tabs
        self.q_tabs = QTabWidget()
        self.q_stat_tab = QPrivateDataWeaponStatTab()
        self.q_tune_tab = QPrivateDataWeaponTuneTab()

        self.q_tabs.addTab(self.q_stat_tab, _(ZhTwEnum.TAB_STAT))
        self.q_tabs.addTab(self.q_tune_tab, _(ZhTwEnum.TAB_TUNE))

        self.layout.addLayout(self.q_weapon_layout)
        self.layout.addWidget(self.q_tabs)

        self.setLayout(self.layout)

    def delete(self):
        weapon_name = self.q_weapon_combobox.currentText()
        if not weapon_name:
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.WEAPON_NAME_MUST_NOT_EMPTY)
            )
            return

        weapon_dir_path = get_weapon_dir_path(weapon_name)
        weapon_stat_fpath = get_weapon_stat_fpath(weapon_name)
        weapon_tune_fpath = get_weapon_rank_fpath(weapon_name)
        if not weapon_dir_path.is_dir():
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                f"'{weapon_dir_path}' {_(ZhTwEnum.PATH_MUST_BE_DIR)}",
            )
            return
        if weapon_stat_fpath.exists():
            weapon_stat_fpath.unlink()
        if weapon_tune_fpath.exists():
            weapon_tune_fpath.unlink()

        weapon_dir_path.rmdir()

        self.load_tabs()
        self.q_weapon_combobox.setCurrentText("")

    def load_tabs(self):
        weapon_name = self.q_weapon_combobox.currentText()
        if not weapon_name:
            return

        self.q_stat_tab.load(weapon_name)
        self.q_tune_tab.load(weapon_name)
