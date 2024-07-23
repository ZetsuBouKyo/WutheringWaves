import sys
from functools import partial
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QCompleter,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import get_row_damage
from ww.model.echo_skill import EchoSkillEnum
from ww.model.monsters import MonstersEnum
from ww.model.resonator_skill import (
    ResonatorSkillBaseAttrEnum,
    ResonatorSkillBonusTypeEnum,
    ResonatorSkillEnum,
)
from ww.model.resonators import (
    CALCULATED_RESONATORS_DMG_BONUS_PREFIX,
    CALCULATED_RESONATORS_DMG_BONUS_SUFFIX,
    CalculatedResonatorsEnum,
    ResonatorsEnum,
)
from ww.model.template import CalculatedTemplateEnum, TemplateEnum
from ww.tables.echo_skill import EchoSkillTable
from ww.tables.monsters import MonstersTable
from ww.tables.resonator_skill import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.template import TemplateTable
from ww.ui.combobox import QCustomComboBox
from ww.utils.number import get_number, get_string


def get_resonator_names() -> List[str]:
    resonators_table = ResonatorsTable()
    names = [name for name in resonators_table.df[ResonatorsEnum.ID].to_list() if name]
    return names


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
        self._input_bonus_magnifier = self._init_input_bonus_magifier()
        self._input_bonus_amplifier = self._init_input_bonus_amplifier()
        self._input_bonus_atk_p = self._init_input_bonus_atk_p()
        self._input_bonus_atk = self._init_input_bonus_atk()
        self._input_bonus_crit_rate = self._init_input_bonus_crit_rate()
        self._input_bonus_crit_dmg = self._init_input_bonus_crit_dmg()
        self._input_bonus_addition = self._init_input_bonus_addition()
        self._input_bonus_skill_dmg_addition = (
            self._init_input_bonus_skill_dmg_addition()
        )
        self._input_bonus_ignore_def = self._init_input_bonus_ignore_def()
        self._button_save = self._init_button_save()

        # Right
        self.layout_right = QVBoxLayout()
        self.layout_right.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self._init_label_result_title()

        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def _init_base(self):
        self._label_width = 200
        self._input_width = 600

        self._echo_skill_table = EchoSkillTable()
        self._monsters_table = MonstersTable()
        self._calculated_template_columns = [e.value for e in CalculatedTemplateEnum]

    def _init_combobox(self, label_name: str, getOptions, currentTextChanged):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel(label_name)
        label.setFixedWidth(self._label_width)
        layout.addWidget(label)

        combobox = QCustomComboBox(getOptions=getOptions)
        combobox.setFixedWidth(self._input_width)
        if currentTextChanged is not None:
            combobox.currentTextChanged.connect(currentTextChanged)  # not working
        layout.addWidget(combobox)

        self.layout_left.addLayout(layout)

        return combobox

    def _combobox_event_update_resonator(self, resonator_id: str):
        if resonator_id == "":
            return

        self._combobox_resonator_skills.clear()

        self._resonator_id = resonator_id
        self._resonators_table = ResonatorsTable()
        self._calculated_resonators_table = CalculatedResonatorsTable()

        self._resonator_name = self._resonators_table.search(
            self._resonator_id, ResonatorsEnum.NAME
        )
        self._resonator_skills_table = ResonatorSkillTable(self._resonator_name)

        # TODO: resonator skill -> row

    def _init_combobox_resonator_ids(self):
        return self._init_combobox(
            "共鳴者", get_resonator_names, self._combobox_event_update_resonator
        )

    def _get_resonator_skills(self):
        if not hasattr(self, "_resonator_skills_table"):
            return []
        if self._resonator_skills_table.df is None:
            return []
        names = [
            name
            for name in self._resonator_skills_table.df[
                ResonatorSkillEnum.SKILL_ID.value
            ].to_list()
            if name
        ]
        return names

    def _combobox_event_update_resonator_skill(self, skill_id: str):
        if not skill_id:
            return
        self._resonator_skill_id = skill_id

    def _init_combobox_resonator_skills(self):
        return self._init_combobox("共鳴者技能", self._get_resonator_skills, None)

    def _get_monster_ids(self):
        names = [
            name
            for name in self._monsters_table.df[MonstersEnum.NAME].to_list()
            if name
        ]
        return names

    def _combobox_event_update_monster_id(self, monster_id: str):
        # TODO: monster name -> monster id
        if not monster_id:
            return

        self._monster_id = monster_id
        self._monster_level = get_number(
            self._monsters_table.search(self._monster_id, MonstersEnum.LEVEL)
        )
        self._monster_def = get_number(
            self._monsters_table.search(self._monster_id, MonstersEnum.DEF)
        )

    def _init_combobox_monster_ids(self):
        return self._init_combobox(
            "怪物", self._get_monster_ids, self._combobox_event_update_monster_id
        )

    def _init_input(self, label_name: str, tooltip: str = None):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel(label_name)
        label.setFixedWidth(self._label_width)
        layout.addWidget(label)

        line = QLineEdit()
        line.setFixedWidth(self._input_width)
        line.setPlaceholderText("")
        if tooltip is not None:
            line.setToolTip(tooltip)
        layout.addWidget(line)

        self.layout_left.addLayout(layout)

        return line

    def _init_input_bonus_magifier(self):
        return self._init_input(
            TemplateEnum.BONUS_MAGNIFIER.value,
            f"計算方式: 1+{TemplateEnum.BONUS_MAGNIFIER.value}",
        )

    def _init_input_bonus_amplifier(self):
        return self._init_input(
            TemplateEnum.BONUS_AMPLIFIER.value,
            f"計算方式: 1+{TemplateEnum.BONUS_AMPLIFIER.value}",
        )

    def _init_input_bonus_atk_p(self):
        return self._init_input(
            TemplateEnum.BONUS_ATK_P.value,
            f"計算方式: 1+{TemplateEnum.BONUS_ATK_P.value}+其他額外攻擊百分比",
        )

    def _init_input_bonus_atk(self):
        return self._init_input(
            TemplateEnum.BONUS_ATK.value,
            f"計算方式: {TemplateEnum.BONUS_ATK.value}+聲骸攻擊+其他攻擊",
        )

    def _init_input_bonus_crit_rate(self):
        return self._init_input(
            TemplateEnum.BONUS_CRIT_RATE.value,
            f"計算方式: {TemplateEnum.BONUS_CRIT_RATE.value}+其他暴擊",
        )

    def _init_input_bonus_crit_dmg(self):
        return self._init_input(
            TemplateEnum.BONUS_CRIT_DMG.value,
            f"計算方式: {TemplateEnum.BONUS_CRIT_DMG.value}+其他暴擊傷害",
        )

    def _init_input_bonus_addition(self):
        return self._init_input(
            TemplateEnum.BONUS_ADDITION.value,
            f"計算方式: {TemplateEnum.BONUS_ADDITION.value}+其他加成區",
        )

    def _init_input_bonus_skill_dmg_addition(self):
        return self._init_input(
            TemplateEnum.BONUS_SKILL_DMG_ADDITION.value,
            f"計算方式: {TemplateEnum.BONUS_SKILL_DMG_ADDITION.value}+招式倍率",
        )

    def _init_input_bonus_ignore_def(self):
        return self._init_input(TemplateEnum.BONUS_IGNORE_DEF.value)

    def _init_input_bonus_reduce_res(self):
        return self._init_input(TemplateEnum.BONUS_REDUCE_RES.value)

    def _init_button_save(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        btn = QPushButton("計算")
        btn.clicked.connect(self._calculate)

        layout.addWidget(btn)
        self.layout_left.addLayout(layout)
        return btn

    def _calculate(self):

        row = {
            TemplateEnum.RESONATOR_NAME.value: resonator_name,
            TemplateEnum.SKILL_ID.value: None,
        }
        get_row_damage()

    def _init_label_result_title(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel("計算結果")
        label.setFixedWidth(self._label_width)
        layout.addWidget(label)

        self.layout_right.addLayout(layout)

    def _init_label_result(self, title: str, result: str):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label_title = QLabel(title)
        label_title.setFixedWidth(self._label_width)
        label_result = QLabel(result)
        label_result.setFixedWidth(self._input_width)

        layout.addWidget(label_title)
        layout.addWidget(label_result)

        self.layout_right.addLayout(layout)
