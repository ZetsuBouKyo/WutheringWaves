import json
import os
from typing import Dict, Optional, Tuple, Union

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ww.crud.resonator import get_resonator_names
from ww.locale import ZhTwEnum, _
from ww.model.resonator import ResonatorStatEnum
from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.resonator import (
    get_resonator_dir_path,
    get_resonator_information_fpath,
    get_resonator_skill_fpath,
    get_resonator_stat_fpath,
)
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.utils.pd import get_empty_df


class QPrivateDataResonatorInformationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.resonator_name_combobox = None

        self.layout = QVBoxLayout()

        # Buttons
        self.q_layout_btns = QHBoxLayout()
        self.q_btn_save = QPushButton(_(ZhTwEnum.SAVE))
        self.q_btn_save.clicked.connect(self.save)
        self.q_btn_load = QPushButton(_(ZhTwEnum.LOAD))
        self.q_btn_load.clicked.connect(self.load)
        self.q_layout_btns.addStretch()
        self.q_layout_btns.addWidget(self.q_btn_save)
        self.q_layout_btns.addWidget(self.q_btn_load)

        self.layout.addLayout(self.q_layout_btns)

        # Tabs
        self.q_tabs = QTabWidget()

        # Skills
        self.q_skills: Dict[str, Dict[str, Optional[Union[QLineEdit, QTextEdit]]]] = {
            _(ZhTwEnum.NORMAL_ATTACK): None,
            _(ZhTwEnum.RESONANCE_SKILL): None,
            _(ZhTwEnum.FORTE_CIRCUIT): None,
            _(ZhTwEnum.RESONANCE_LIBERATION): None,
            _(ZhTwEnum.INTRO_SKILL): None,
            _(ZhTwEnum.OUTRO_SKILL): None,
        }
        self.q_skill_tab = self.get_tab(self.q_skills)
        self.q_tabs.addTab(self.q_skill_tab, _(ZhTwEnum.TAB_SKILL))

        # Inherent skills
        self.q_inherent_skills: Dict[
            str, Dict[str, Optional[Union[QLineEdit, QTextEdit]]]
        ] = {
            _(ZhTwEnum.INHERENT_SKILL_1): None,
            _(ZhTwEnum.INHERENT_SKILL_2): None,
        }
        self.q_inherent_skill_tab = self.get_tab(self.q_inherent_skills)
        self.q_tabs.addTab(self.q_inherent_skill_tab, _(ZhTwEnum.TAB_INHERENT_SKILL))

        # Chains
        self.q_chains: Dict[str, Dict[str, Optional[Union[QLineEdit, QTextEdit]]]] = {
            _(ZhTwEnum.CHAIN_1): None,
            _(ZhTwEnum.CHAIN_2): None,
            _(ZhTwEnum.CHAIN_3): None,
            _(ZhTwEnum.CHAIN_4): None,
            _(ZhTwEnum.CHAIN_5): None,
            _(ZhTwEnum.CHAIN_6): None,
        }
        self.q_chain_tab = self.get_tab(self.q_chains)
        self.q_tabs.addTab(self.q_chain_tab, _(ZhTwEnum.TAB_CHAIN))

        self.layout.addWidget(self.q_tabs)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def get_label_layout(self, name) -> QVBoxLayout:
        layout = QVBoxLayout()
        label = QLabel(name)
        label.setFixedWidth(100)
        label.setFixedHeight(40)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignTop)
        return layout

    def get_text_components(self) -> Tuple[QVBoxLayout, QLineEdit, QTextEdit]:
        layout = QVBoxLayout()
        text_line = QLineEdit()
        text_line.setFixedHeight(40)
        text_edit = QTextEdit()
        layout.addWidget(text_line)
        layout.addWidget(text_edit)
        layout.setAlignment(Qt.AlignTop)
        return layout, text_line, text_edit

    def get_tab(self, str2qt: Dict[str, QTextEdit]) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout()
        for label_name in str2qt.keys():
            h_layout = QHBoxLayout()

            label_layout = self.get_label_layout(label_name)
            text_layout, text_line, text_edit = self.get_text_components()
            str2qt[label_name] = {
                _(ZhTwEnum.NAME): text_line,
                _(ZhTwEnum.DESCRIPTION): text_edit,
            }

            h_layout.addLayout(label_layout)
            h_layout.addLayout(text_layout, 1)

            layout.addLayout(h_layout)
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def set_resonator_name_combobox(self, combobox: QAutoCompleteComboBox):
        self.resonator_name_combobox = combobox

    def set_text(self, key: str, values: Dict[str, str]):
        str2qts = [self.q_skills, self.q_inherent_skills, self.q_chains]
        for str2qt in str2qts:
            text_components = str2qt.get(key, None)
            if text_components is None:
                continue

            text_line = text_components.get(_(ZhTwEnum.NAME), None)
            text_edit = text_components.get(_(ZhTwEnum.DESCRIPTION), None)
            text_line_str = values.get(_(ZhTwEnum.NAME), None)
            text_edit_str = values.get(_(ZhTwEnum.DESCRIPTION), None)
            if text_line is not None and text_line_str is not None:
                text_line.setText(text_line_str)

            if text_edit is not None and text_edit_str is not None:
                text_edit.setText(text_edit_str)

    def get_data(self) -> Dict[str, Dict[str, str]]:
        data = {}
        str2qts = [self.q_skills, self.q_inherent_skills, self.q_chains]
        for str2qt in str2qts:
            for title_name, line in str2qt.items():
                data[title_name] = {}
                for key, value in line.items():
                    if isinstance(value, QLineEdit):
                        data[title_name][key] = value.text()
                    elif isinstance(value, QTextEdit):
                        data[title_name][key] = value.toPlainText()
        return data

    def load(self):
        if not self.resonator_name_combobox:
            return
        resonator_name = self.resonator_name_combobox.currentText()

        json_fpath = get_resonator_information_fpath(resonator_name)
        if json_fpath is None:
            return

        if not json_fpath.exists():
            return

        with json_fpath.open(mode="r", encoding="utf-8") as fp:
            data: dict = json.load(fp)
        for key, values in data.items():
            self.set_text(key, values)

    def save(self):
        if not self.resonator_name_combobox:
            return
        resonator_name = self.resonator_name_combobox.currentText()
        if not resonator_name:
            return

        data = self.get_data()
        json_fpath = get_resonator_information_fpath(resonator_name)
        if json_fpath is None:
            return
        if json_fpath.is_dir():
            return

        os.makedirs(json_fpath.parent, exist_ok=True)
        with json_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)


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
        self.q_resonator_label = QLabel(_(ZhTwEnum.NAME))
        self.q_resonator_label.setFixedHeight(40)
        self.q_resonator_combobox = QAutoCompleteComboBox(
            getOptions=get_resonator_names
        )
        self.q_resonator_combobox.setFixedHeight(40)
        self.q_resonator_combobox.setFixedWidth(150)
        self.q_resonator_combobox.currentTextChanged.connect(self.load_tabs)
        self.q_delete_btn = QPushButton(_(ZhTwEnum.DELETE))
        self.q_delete_btn.clicked.connect(self.delete)

        self.q_resonator_layout.addWidget(self.q_resonator_label)
        self.q_resonator_layout.addWidget(self.q_resonator_combobox)
        self.q_resonator_layout.addStretch()
        self.q_resonator_layout.addWidget(self.q_delete_btn)

        # Tabs
        self.q_tabs = QTabWidget()
        self.q_information_tab = QPrivateDataResonatorInformationTab()
        self.q_stat_tab = QPrivateDataResonatorStatTab()
        self.q_skill_tab = QPrivateDataResonatorSkillTab()

        self.q_tabs.addTab(self.q_information_tab, _(ZhTwEnum.TAB_INFORMATION))
        self.q_tabs.addTab(self.q_stat_tab, _(ZhTwEnum.TAB_STAT))
        self.q_tabs.addTab(self.q_skill_tab, _(ZhTwEnum.TAB_SKILL))

        self.layout.addLayout(self.q_resonator_layout)
        self.layout.addWidget(self.q_tabs)

        self.setLayout(self.layout)

    def delete(self):
        resonator_name = self.q_resonator_combobox.currentText()
        if not resonator_name:
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.RESONATOR_NAME_MUST_NOT_EMPTY)
            )
            return

        resonator_dir_path = get_resonator_dir_path(resonator_name)

        resonator_information_fpath = get_resonator_information_fpath(resonator_name)
        resonator_stat_fpath = get_resonator_stat_fpath(resonator_name)
        resonator_skill_fpath = get_resonator_skill_fpath(resonator_name)
        fpaths = [
            resonator_information_fpath,
            resonator_stat_fpath,
            resonator_skill_fpath,
        ]
        if not resonator_dir_path.is_dir():
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                f"'{resonator_dir_path}' {_(ZhTwEnum.PATH_MUST_BE_DIR)}",
            )
            return
        for fpath in fpaths:
            if fpath.exists():
                fpath.unlink()

        resonator_dir_path.rmdir()

        self.load_tabs()
        self.q_resonator_combobox.setCurrentText("")

    def load_tabs(self):
        resonator_name = self.q_resonator_combobox.currentText()
        if not resonator_name:
            return

        self.q_information_tab.set_resonator_name_combobox(self.q_resonator_combobox)
        self.q_information_tab.load()
        self.q_stat_tab.load(resonator_name)
        self.q_skill_tab.load(resonator_name)
