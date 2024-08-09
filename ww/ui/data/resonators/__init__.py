from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QCompleter, QProgressBar, QTableWidgetItem

from ww.crud.resonator import (
    get_resonator_chains,
    get_resonator_inherent_skills,
    get_resonator_names,
)
from ww.crud.weapon import get_weapon_names, get_weapon_ranks
from ww.model.echoes import EchoesEnum
from ww.model.resonators import ResonatorsEnum
from ww.tables.calculated_resonators import calc
from ww.tables.echoes import EchoesTable
from ww.tables.resonators import RESONATORS_PATH, ResonatorsTable
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QDraggableTableWidget


def get_echoes() -> List[str]:
    echoes_table = EchoesTable()
    echoes = echoes_table.df[EchoesEnum.ID]
    return echoes.to_list()


def get_resonator_skill_levels() -> List[str]:
    return [str(i) for i in range(1, 11)]


def get_levels() -> List[str]:
    levels = [str(i) for i in range(10, 100, 10)] + [
        "1",
        "20+",
        "40+",
        "60+",
        "70+",
        "80+",
    ]
    levels.sort()
    return levels


class QResonatorsTable(QDraggableTableWidget):
    def __init__(self):
        resonators_table = ResonatorsTable()

        data = resonators_table.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        self._init_combobox()
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorsEnum.ID.value,
            column_names=resonators_table.df.columns,
        )

    def _init_column_width(self):
        cols = [
            self.get_column_id(ResonatorsEnum.ID.value),
            self.get_column_id(ResonatorsEnum.ECHO_1.value),
            self.get_column_id(ResonatorsEnum.ECHO_2.value),
            self.get_column_id(ResonatorsEnum.ECHO_3.value),
            self.get_column_id(ResonatorsEnum.ECHO_4.value),
            self.get_column_id(ResonatorsEnum.ECHO_5.value),
        ]
        for col in cols:
            self.setColumnWidth(col, 400)

    def _init_combobox(self):
        self._echoes = get_echoes()
        self._resonator_names = get_resonator_names()
        self._resonator_levels = get_levels()
        self._resonator_chains = get_resonator_chains()
        self._resonator_skill_levels = get_resonator_skill_levels()
        self._resonator_inherent_skills = get_resonator_inherent_skills()
        self._weapon_names = get_weapon_names()
        self._weapon_levels = get_levels()
        self._weapon_ranks = get_weapon_ranks()

    def get_row_id(self, row: List[str]) -> str:
        _id = []

        _prefix_i = self.get_column_id(ResonatorsEnum.PREFIX.value)
        _prefix = row[_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _chain_i = self.get_column_id(ResonatorsEnum.RESONANCE_CHAIN.value)
        _chain = row[_chain_i]
        if _chain:
            _id.append(f"{_chain}鏈")

        _level_i = self.get_column_id(ResonatorsEnum.LEVEL.value)
        _level = row[_level_i]
        _name_i = self.get_column_id(ResonatorsEnum.NAME.value)
        _name = row[_name_i]
        if _name:
            _id.append(_level + _name)

        _weapon_rank_i = self.get_column_id(ResonatorsEnum.WEAPON_RANK.value)
        _weapon_rank = row[_weapon_rank_i]
        if _weapon_rank:
            _id.append(f"{_weapon_rank}振")

        _weapon_level_i = self.get_column_id(ResonatorsEnum.WEAPON_LEVEL.value)
        _weapon_level = row[_weapon_level_i]
        _weapon_name_i = self.get_column_id(ResonatorsEnum.WEAPON_NAME.value)
        _weapon_name = row[_weapon_name_i]
        if _weapon_name:
            _id.append(_weapon_level + _weapon_name)

        _suffix_i = self.get_column_id(ResonatorsEnum.SUFFIX.value)
        _suffix = row[_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def _update_row_id(self, row: int, col: int, value: str):
        # prefix_col = self.get_column_id(ResonatorsEnum.PREFIX.value)
        # suffix_col = self.get_column_id(ResonatorsEnum.SUFFIX.value)
        # if prefix_col == col or suffix_col == col:
        #     return
        # id_col = self.get_column_id(ResonatorsEnum.ID.value)
        # self.data[row][col] = value
        # id = self.get_row_id(row)
        # self.set_id_cell(id, row, id_col)
        ...

    def _update_row_id_by_combobox(self, row: int, col: int, values: List[str], i: int):
        try:
            self._update_row_id(row, col, values[i])
        except IndexError:
            ...

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == ResonatorsEnum.ID.value:
            self.set_id_cell(value, row, col)
        elif self.column_names[col] == ResonatorsEnum.NAME.value:
            self.set_combobox(
                row,
                col,
                value,
                self._resonator_names,
                currentIndexChanged=self._update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.LEVEL.value:
            self.set_combobox(
                row,
                col,
                value,
                self._resonator_levels,
                currentIndexChanged=self._update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_CHAIN.value:
            self.set_combobox(
                row,
                col,
                value,
                self._resonator_chains,
                currentIndexChanged=self._update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.NORMAL_ATTACK_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_SKILL_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_LIBERATION_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.FORTE_CIRCUIT_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.INTRO_SKILL_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.OUTRO_SKILL_LV.value:
            self.set_combobox(row, col, value, ["1"])
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_1.value:
            self.set_combobox(row, col, value, self._resonator_inherent_skills)
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_2.value:
            self.set_combobox(row, col, value, self._resonator_inherent_skills)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_NAME.value:
            self.set_combobox(
                row,
                col,
                value,
                self._weapon_names,
                currentIndexChanged=self._update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.WEAPON_LEVEL.value:
            self.set_combobox(
                row,
                col,
                value,
                self._weapon_levels,
                currentIndexChanged=self._update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.WEAPON_RANK.value:
            self.set_combobox(
                row,
                col,
                value,
                self._weapon_ranks,
                currentIndexChanged=self._update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.ECHO_1.value:
            self.set_combobox(row, col, value, self._echoes, getOptions=get_echoes)
        elif self.column_names[col] == ResonatorsEnum.ECHO_2.value:
            self.set_combobox(row, col, value, self._echoes, getOptions=get_echoes)
        elif self.column_names[col] == ResonatorsEnum.ECHO_3.value:
            self.set_combobox(row, col, value, self._echoes, getOptions=get_echoes)
        elif self.column_names[col] == ResonatorsEnum.ECHO_4.value:
            self.set_combobox(row, col, value, self._echoes, getOptions=get_echoes)
        elif self.column_names[col] == ResonatorsEnum.ECHO_5.value:
            self.set_combobox(row, col, value, self._echoes, getOptions=get_echoes)
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)

    def load(self):
        resonators_table = ResonatorsTable()
        self.data = resonators_table.df.values.tolist()
