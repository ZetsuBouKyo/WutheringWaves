import sys
from functools import partial

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

from ww.crud.resonator import get_resonator_names
from ww.locale import ZhHantEnum, _
from ww.model.resonator import ResonatorStatEnum
from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.resonator import (
    get_resonator_dir_path,
    get_resonator_skill_fpath,
    get_resonator_stat_fpath,
)
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.utils.pd import get_empty_df


class QPrivateDataResonatorStatTable(QDraggableTableWidget):
    def __init__(self):
        column_names = [e.value for e in ResonatorStatEnum]
        df = get_empty_df(column_names)
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorStatEnum.LEVEL.value,
            column_names=column_names,
        )


class QPrivateDataResonatorStatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataResonatorStatTable()
        self.q_tsv = QDraggableTsvTableWidget(self.q_table)
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)

    def load(self, resonator_name: str):
        tsv_fpath = get_resonator_stat_fpath(resonator_name)
        if tsv_fpath is None:
            return

        self.q_tsv.set_tsv_fpath(tsv_fpath)
        self.q_tsv.load(is_confirmation=False)


class QPrivateDataResonatorSkillTable(QDraggableTableWidget):
    def __init__(self):
        column_names = [e.value for e in ResonatorSkillEnum]
        df = get_empty_df(column_names)
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorSkillEnum.PRIMARY_KEY.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 400)


class QPrivateDataResonatorSkillTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataResonatorSkillTable()
        self.q_tsv = QDraggableTsvTableWidget(self.q_table)
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)

    def load(self, resonator_name: str):
        tsv_fpath = get_resonator_skill_fpath(resonator_name)
        if tsv_fpath is None:
            return

        self.q_tsv.set_tsv_fpath(tsv_fpath)
        self.q_tsv.load(is_confirmation=False)


class QPrivateDataResonatorTabs(QWidget):
    def __init__(self):
        super().__init__()
        self._last_resonator = None
        self._changed = True

        self.layout = QVBoxLayout()

        self.q_resonator_layout = QHBoxLayout()
        self.q_resonator_label = QLabel(_(ZhHantEnum.NAME))
        self.q_resonator_label.setFixedHeight(40)
        self.q_resonator_combobox = QCustomComboBox(getOptions=get_resonator_names)
        self.q_resonator_combobox.setFixedHeight(40)
        self.q_resonator_combobox.setFixedWidth(150)
        self.q_resonator_combobox.currentTextChanged.connect(self.load_tabs)
        self.q_delete_btn = QPushButton(_(ZhHantEnum.DELETE))
        self.q_delete_btn.clicked.connect(self.delete)

        self.q_resonator_layout.addWidget(self.q_resonator_label)
        self.q_resonator_layout.addWidget(self.q_resonator_combobox)
        self.q_resonator_layout.addStretch()
        self.q_resonator_layout.addWidget(self.q_delete_btn)

        # Tabs
        self.q_tabs = QTabWidget()
        self.q_stat_tab = QPrivateDataResonatorStatTab()
        self.q_skill_tab = QPrivateDataResonatorSkillTab()

        self.q_tabs.addTab(self.q_stat_tab, _(ZhHantEnum.TAB_STAT))
        self.q_tabs.addTab(self.q_skill_tab, _(ZhHantEnum.TAB_SKILL))

        self.layout.addLayout(self.q_resonator_layout)
        self.layout.addWidget(self.q_tabs)

        self.setLayout(self.layout)

    def delete(self):
        resonator_name = self.q_resonator_combobox.currentText()
        if not resonator_name:
            QMessageBox.warning(
                self, _(ZhHantEnum.WARNING), _(ZhHantEnum.RESONATOR_NAME_MUST_NOT_EMPTY)
            )
            return

        resonator_dir_path = get_resonator_dir_path(resonator_name)
        resonator_stat_fpath = get_resonator_stat_fpath(resonator_name)
        resonator_skill_fpath = get_resonator_skill_fpath(resonator_name)
        if not resonator_dir_path.is_dir():
            QMessageBox.warning(
                self,
                _(ZhHantEnum.WARNING),
                f"'{resonator_dir_path}' {_(ZhHantEnum.PATH_MUST_BE_DIR)}",
            )
            return
        if resonator_stat_fpath.exists():
            resonator_stat_fpath.unlink()
        if resonator_skill_fpath.exists():
            resonator_skill_fpath.unlink()
        resonator_dir_path.rmdir()

        self.load_tabs()
        self.q_resonator_combobox.setCurrentText("")

    def load_tabs(self):
        resonator_name = self.q_resonator_combobox.currentText()
        if not resonator_name:
            return

        self.q_stat_tab.load(resonator_name)
        self.q_skill_tab.load(resonator_name)
