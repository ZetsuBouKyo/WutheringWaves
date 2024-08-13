from decimal import Decimal
from typing import Dict, Optional, Union

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import get_json_row_damage
from ww.crud.resonator import get_resonator_ids
from ww.locale import ZhTwEnum, _
from ww.model.monsters import MonstersEnum
from ww.model.resonator_skill import ResonatorSkillEnum
from ww.model.resonators import ResonatorsEnum
from ww.model.template import (
    CalculatedTemplateEnum,
    CalculatedTemplateRowModel,
    TemplateBuffTableRowModel,
    TemplateRowBuffTypeEnum,
    TemplateRowModel,
)
from ww.tables.echo import EchoSkillTable
from ww.tables.monster import MonstersTable
from ww.tables.resonator import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.table.cell import set_uneditable_cell
from ww.utils.number import get_number


class QDamageSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        # Left
        self.layout_left = QVBoxLayout()
        self.layout_left.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self._init_base()
        self._combobox_resonator_ids = self._init_combobox_resonator_ids()
        self._combobox_resonator_skills = self._init_combobox_resonator_skills()
        self._combobox_monster_ids = self._init_combobox_monster_ids()

        # Buffs
        self.q_buffs: Dict[str, QLineEdit] = {}
        for e in TemplateRowBuffTypeEnum:
            label_name = f"[{_(ZhTwEnum.BUFF)}]{e.value}"
            q_buff = self._init_input(label_name)
            self.q_buffs[e.value] = q_buff

        self._button_save = self._init_button_save()

        # Right
        self.layout_right = QVBoxLayout()
        self.layout_right.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self._init_label_result_title()
        self._init_table_results()

        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def _init_base(self):
        self._label_width = 200
        self._input_width = 600

        self._echo_skill_table = EchoSkillTable()
        self._calculated_template_columns = [e.value for e in CalculatedTemplateEnum]

    def _init_combobox(
        self, label_name: str, getOptions, currentTextChanged
    ) -> QAutoCompleteComboBox:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel(label_name)
        label.setFixedWidth(self._label_width)
        layout.addWidget(label)

        combobox = QAutoCompleteComboBox(getOptions=getOptions)
        combobox.setFixedWidth(self._input_width)
        combobox.setFixedHeight(40)
        if currentTextChanged is not None:
            combobox.currentTextChanged.connect(currentTextChanged)  # not working
        layout.addWidget(combobox)

        self.layout_left.addLayout(layout)

        return combobox

    def _combobox_event_update_resonator(self, resonator_id: str):
        if resonator_id == "":
            return

        self._combobox_resonator_skills.clear()

        # TODO: resonator skill -> row

    def _init_combobox_resonator_ids(self) -> QAutoCompleteComboBox:
        return self._init_combobox(
            "共鳴者", get_resonator_ids, self._combobox_event_update_resonator
        )

    def get_resonator_id(self) -> str:
        return self._combobox_resonator_ids.currentText()

    def _get_resonator_skills(self):
        resonator_id = self._combobox_resonator_ids.currentText()
        if not resonator_id:
            return []
        resonators_table = ResonatorsTable()
        resonator_name = resonators_table.search(resonator_id, ResonatorsEnum.NAME)
        if resonator_name is None:
            return []

        resonator_skills_table = ResonatorSkillTable(resonator_name)
        if resonator_skills_table.df is None:
            return []

        names = [
            name
            for name in resonator_skills_table.df[
                ResonatorSkillEnum.PRIMARY_KEY.value
            ].to_list()
            if name
        ]
        return names

    def _init_combobox_resonator_skills(self) -> QAutoCompleteComboBox:
        return self._init_combobox(
            "共鳴者技能",
            self._get_resonator_skills,
            None,
        )

    def _get_monster_ids(self):
        monsters_table = MonstersTable()
        names = [
            name for name in monsters_table.df[MonstersEnum.NAME].to_list() if name
        ]
        return names

    def _init_combobox_monster_ids(self) -> QAutoCompleteComboBox:
        return self._init_combobox("怪物", self._get_monster_ids, None)

    def get_monster_id(self) -> str:
        monster_id = self._combobox_monster_ids.currentText()
        return monster_id

    def _init_input(self, label_name: str, tooltip: str = None) -> QLineEdit:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel(label_name)
        label.setFixedWidth(self._label_width)
        label.setFixedHeight(40)
        layout.addWidget(label)

        line = QLineEdit()
        line.setFixedWidth(self._input_width)
        line.setFixedHeight(40)
        line.setPlaceholderText("")
        if tooltip is not None:
            line.setToolTip(tooltip)
        layout.addWidget(line)

        self.layout_left.addLayout(layout)

        return line

    def _init_button_save(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        btn = QPushButton(_(ZhTwEnum.CALCULATE))
        btn.clicked.connect(self._calculate)

        layout.addWidget(btn)
        self.layout_left.addLayout(layout)
        return btn

    def _calculate(self):
        resonators_table = ResonatorsTable()
        calculated_resonators_table = CalculatedResonatorsTable()

        resonator_id = self.get_resonator_id()
        resonator_skill_id = self._combobox_resonator_skills.currentText()
        resonator_name = resonators_table.search(resonator_id, ResonatorsEnum.NAME)
        monster_id = self.get_monster_id()
        if not resonator_name or not resonator_skill_id or not monster_id:
            return

        buffs = []
        for buff_type in self.q_buffs.keys():
            q_buff = self.q_buffs[buff_type]
            value = str(get_number(q_buff.text()))
            buff = TemplateBuffTableRowModel(type=buff_type, value=value, stack="1")
            buffs.append(buff)
        row = TemplateRowModel(
            resonator_name=resonator_name,
            real_dmg_no_crit="",
            real_dmg_crit="",
            action="",
            skill_id=resonator_skill_id,
            skill_bonus_type="",
            buffs=buffs,
        )

        monsters_table = MonstersTable()
        monster_level = get_number(
            monsters_table.search(monster_id, MonstersEnum.LEVEL)
        )
        monster_def = get_number(monsters_table.search(monster_id, MonstersEnum.DEF))
        results = get_json_row_damage(
            row,
            resonator_id,
            resonator_name,
            monster_id,
            monster_level,
            monster_def,
            resonators_table,
            calculated_resonators_table,
            self._echo_skill_table,
            monsters_table,
        )

        self._set_table_results(results)

    def _init_label_result_title(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel("計算結果")
        label.setFixedWidth(self._label_width)
        label.setFixedHeight(40)
        layout.addWidget(label)

        self.layout_right.addLayout(layout)

    def _set_table_results(self, results: Optional[CalculatedTemplateRowModel]):
        if results is None:
            return
        damage = None
        damage_no_crit = None
        damage_crit = None
        if results.damage is not None:
            damage = f"{results.damage:.2f}"
        if results.damage_no_crit is not None:
            damage_no_crit = f"{results.damage_no_crit:.2f}"
        if results.damage_crit is not None:
            damage_crit = f"{results.damage_crit:.2f}"

        data = {
            _(ZhTwEnum.RESULT_RESONATOR_NAME): results.resonator_name,
            _(ZhTwEnum.RESULT_SKILL_ID): results.skill_id,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_LEVEL): results.resonator_skill_level,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_ELEMENT): results.resonator_skill_element,
            _(
                ZhTwEnum.RESULT_RESONATOR_SKILL_BASE_ATTR
            ): results.resonator_skill_base_attr,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_TYPE): results.resonator_skill_type,
            _(
                ZhTwEnum.RESULT_RESONATOR_SKILL_TYPE_BONUS
            ): results.resonator_skill_type_bonus,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_DMG): results.resonator_skill_dmg,
            _(ZhTwEnum.RESULT_ECHO_ELEMENT): results.echo_element,
            _(ZhTwEnum.RESULT_ECHO_SKILL_DMG): results.echo_skill_dmg,
            _(ZhTwEnum.RESULT_DAMAGE): damage,
            _(ZhTwEnum.RESULT_DAMAGE_NO_CRIT): damage_no_crit,
            _(ZhTwEnum.RESULT_DAMAGE_CRIT): damage_crit,
            _(ZhTwEnum.RESULT_ELEMENT): results.final_element,
            _(ZhTwEnum.RESULT_BONUS_TYPE): results.final_bonus_type,
            _(ZhTwEnum.RESULT_SKILL_DMG): results.final_skill_dmg,
            _(ZhTwEnum.RESULT_HP): results.final_hp,
            _(ZhTwEnum.RESULT_HP_ADDITION): results.final_hp_addition,
            _(ZhTwEnum.RESULT_HP_P): results.final_hp_p,
            _(ZhTwEnum.RESULT_ATK): results.final_atk,
            _(ZhTwEnum.RESULT_ATK_ADDITION): results.final_atk_addition,
            _(ZhTwEnum.RESULT_ATK_P): results.final_atk_p,
            _(ZhTwEnum.RESULT_DEF): results.final_def,
            _(ZhTwEnum.RESULT_DEF_ADDITION): results.final_def_addition,
            _(ZhTwEnum.RESULT_DEF_P): results.final_def_p,
            _(ZhTwEnum.RESULT_CRIT_RATE): results.final_crit_rate,
            _(ZhTwEnum.RESULT_CRIT_DMG): results.final_crit_dmg,
            _(ZhTwEnum.RESULT_BONUS): results.final_bonus,
            _(ZhTwEnum.RESULT_MONSTER_LEVEL): results.monster_level,
            _(ZhTwEnum.RESULT_MONSTER_DEF): results.monster_def,
            _(ZhTwEnum.RESULT_MONSTER_RES): results.monster_res,
        }
        for i, row_name in enumerate(data.keys()):
            value = data.get(row_name, None)
            if value is None:
                value = ""
            value = str(value)

            set_uneditable_cell(self.table, i, 0, row_name)
            set_uneditable_cell(self.table, i, 1, value)

    def _init_table_results(self):
        layout = QHBoxLayout()
        self.table_row = len(CalculatedTemplateRowModel.model_fields)
        self.table_col = 2
        self.table = QTableWidget(self.table_row, self.table_col)

        self.table.setColumnWidth(0, 200)

        results = CalculatedTemplateRowModel()
        self._set_table_results(results)

        layout.addWidget(self.table)
        self.layout_right.addLayout(layout)
