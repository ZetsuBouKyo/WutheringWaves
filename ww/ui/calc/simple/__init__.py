from typing import Dict, Optional

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
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
from ww.ui.widget import ScrollableWidget
from ww.utils.number import get_number


class QDamageSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.init_results()

        self.layout = QVBoxLayout()
        self.init_calculate_button(self.layout)

        self.two_columns_layout = QHBoxLayout()
        self._label_width = 200

        # Left
        self.left_layout = QVBoxLayout()
        self.init_left_layout(self.left_layout)

        # Right
        self.right_layout = QVBoxLayout()
        self.init_result_labels(self.right_layout)

        self.two_columns_layout.addLayout(self.left_layout, 1)
        self.two_columns_layout.addLayout(self.right_layout, 1)

        self.layout.addLayout(self.two_columns_layout)
        self.setLayout(self.layout)

    def init_results(self):
        self.q_result_labels: Dict[str, Optional[QLabel]] = {
            _(ZhTwEnum.RESULT_RESONATOR_NAME): None,
            _(ZhTwEnum.RESULT_SKILL_ID): None,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_LEVEL): None,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_ELEMENT): None,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_BASE_ATTR): None,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_TYPE): None,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_TYPE_BONUS): None,
            _(ZhTwEnum.RESULT_RESONATOR_SKILL_DMG): None,
            _(ZhTwEnum.RESULT_ECHO_ELEMENT): None,
            _(ZhTwEnum.RESULT_ECHO_SKILL_DMG): None,
            _(ZhTwEnum.RESULT_DAMAGE): None,
            _(ZhTwEnum.RESULT_DAMAGE_NO_CRIT): None,
            _(ZhTwEnum.RESULT_DAMAGE_CRIT): None,
            _(ZhTwEnum.RESULT_ELEMENT): None,
            _(ZhTwEnum.RESULT_BONUS_TYPE): None,
            _(ZhTwEnum.RESULT_SKILL_DMG): None,
            _(ZhTwEnum.RESULT_HP): None,
            _(ZhTwEnum.RESULT_HP_ADDITION): None,
            _(ZhTwEnum.RESULT_HP_P): None,
            _(ZhTwEnum.RESULT_ATK): None,
            _(ZhTwEnum.RESULT_ATK_ADDITION): None,
            _(ZhTwEnum.RESULT_ATK_P): None,
            _(ZhTwEnum.RESULT_DEF): None,
            _(ZhTwEnum.RESULT_DEF_ADDITION): None,
            _(ZhTwEnum.RESULT_DEF_P): None,
            _(ZhTwEnum.RESULT_CRIT_RATE): None,
            _(ZhTwEnum.RESULT_CRIT_DMG): None,
            _(ZhTwEnum.RESULT_BONUS): None,
            _(ZhTwEnum.RESULT_MONSTER_LEVEL): None,
            _(ZhTwEnum.RESULT_MONSTER_DEF): None,
            _(ZhTwEnum.RESULT_MONSTER_RES): None,
        }

    def init_left_layout(self, layout: QVBoxLayout):
        q_left = QWidget()
        q_left_layout = QVBoxLayout()
        self.q_resonator_id_combobox = self.init_resonator_id_combobox(q_left_layout)
        self.q_resonator_skill_combobox = self.init_resonator_skill_combobox(
            q_left_layout
        )
        self.q_monster_id_combobox = self.init_monster_id_combobox(q_left_layout)

        # Buffs
        self.q_buffs: Dict[str, QLineEdit] = {}
        for e in TemplateRowBuffTypeEnum:
            label_name = f"[{_(ZhTwEnum.BUFF)}]{e.value}"
            q_buff = self.init_input(q_left_layout, label_name)
            self.q_buffs[e.value] = q_buff

        q_left.setLayout(q_left_layout)

        q_left_scrollable = ScrollableWidget(q_left)
        layout.addWidget(q_left_scrollable, 1)

    def init_combobox(
        self,
        parent_layout: QVBoxLayout,
        label_name: str,
        getOptions,
        currentTextChanged,
    ) -> QAutoCompleteComboBox:
        layout = QHBoxLayout()

        label = QLabel(label_name)
        label.setFixedWidth(self._label_width)
        layout.addWidget(label)

        combobox = QAutoCompleteComboBox(getOptions=getOptions)
        combobox.setFixedHeight(40)
        if currentTextChanged is not None:
            combobox.currentTextChanged.connect(currentTextChanged)  # not working
        layout.addWidget(combobox, 1)
        parent_layout.addLayout(layout)

        return combobox

    def clear_resonator_skill_combobox(self, resonator_id: str):
        if resonator_id == "":
            return

        self.q_resonator_skill_combobox.clear()

        # TODO: resonator skill -> row

    def init_resonator_id_combobox(
        self, parent_layout: QVBoxLayout
    ) -> QAutoCompleteComboBox:
        return self.init_combobox(
            parent_layout,
            "共鳴者",
            get_resonator_ids,
            self.clear_resonator_skill_combobox,
        )

    def get_resonator_id(self) -> str:
        return self.q_resonator_id_combobox.currentText()

    def get_resonator_skills(self):
        resonator_id = self.q_resonator_id_combobox.currentText()
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

    def init_resonator_skill_combobox(
        self, parent_layout: QVBoxLayout
    ) -> QAutoCompleteComboBox:
        return self.init_combobox(
            parent_layout,
            "共鳴者技能",
            self.get_resonator_skills,
            None,
        )

    def get_monster_ids(self):
        monsters_table = MonstersTable()
        names = [
            name for name in monsters_table.df[MonstersEnum.NAME].to_list() if name
        ]
        return names

    def init_monster_id_combobox(
        self, parent_layout: QVBoxLayout
    ) -> QAutoCompleteComboBox:
        return self.init_combobox(parent_layout, "怪物", self.get_monster_ids, None)

    def get_monster_id(self) -> str:
        monster_id = self.q_monster_id_combobox.currentText()
        return monster_id

    def init_input(
        self, parent_layout: QVBoxLayout, label_name: str, tooltip: str = None
    ) -> QLineEdit:
        layout = QHBoxLayout()

        label = QLabel(label_name)
        label.setFixedWidth(self._label_width)
        label.setFixedHeight(40)
        layout.addWidget(label)

        line = QLineEdit()
        line.setFixedHeight(40)
        line.setPlaceholderText("")
        if tooltip is not None:
            line.setToolTip(tooltip)
        layout.addWidget(line, 1)
        parent_layout.addLayout(layout)

        return line

    def init_calculate_button(self, parent_layout: QVBoxLayout) -> QPushButton:
        layout = QHBoxLayout()

        btn = QPushButton(_(ZhTwEnum.CALCULATE))
        btn.clicked.connect(self.calculate)

        layout.addStretch()
        layout.addWidget(btn)
        parent_layout.addLayout(layout)
        return btn

    def calculate(self):
        resonators_table = ResonatorsTable()
        calculated_resonators_table = CalculatedResonatorsTable()

        resonator_id = self.get_resonator_id()
        resonator_skill_id = self.q_resonator_skill_combobox.currentText()
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
        echo_skill_table = EchoSkillTable()
        results = get_json_row_damage(
            row,
            resonator_id,
            resonator_name,
            monster_id,
            monster_level,
            monster_def,
            resonators_table,
            calculated_resonators_table,
            echo_skill_table,
            monsters_table,
        )
        if results is None:
            results = CalculatedTemplateRowModel()

        self.set_results(self.sub_right_layout, results)

    def init_result_label(
        self, parent_layout: QVBoxLayout, key: str, value: str
    ) -> QLabel:
        layout = QHBoxLayout()

        key_label = QLabel(key)
        key_label.setFixedWidth(self._label_width)
        key_label.setFixedHeight(40)
        layout.addWidget(key_label)

        value_label = QLabel(value)
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        value_label.setCursor(Qt.IBeamCursor)
        value_label.setFixedHeight(40)
        layout.addWidget(value_label, 1)

        parent_layout.addLayout(layout)
        return value_label

    def set_results(
        self, parent_layout: QVBoxLayout, results: CalculatedTemplateRowModel
    ):
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
        for i, key in enumerate(data.keys()):
            value = data.get(key, None)
            if value is None:
                value = ""
            value = str(value)
            q_label = self.q_result_labels.get(key, None)
            if q_label is None:
                q_label = self.init_result_label(parent_layout, key, value)
                self.q_result_labels[key] = q_label
            else:
                q_label.setText(value)

    def init_result_labels(self, parent_layout: QVBoxLayout):
        results = CalculatedTemplateRowModel()

        q_result_labels = QWidget()
        self.sub_right_layout = QVBoxLayout()
        self.set_results(self.sub_right_layout, results)
        q_result_labels.setLayout(self.sub_right_layout)

        parent_layout.addWidget(ScrollableWidget(q_result_labels))
