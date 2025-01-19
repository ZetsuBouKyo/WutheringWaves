from collections import OrderedDict
from enum import Enum
from typing import List

from PySide2.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ww.calc.damage import Damage
from ww.calc.simulated_resonators import SimulatedResonators
from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.model.resonator_skill import ResonatorSkillTypeEnum
from ww.model.template import (
    CalculatedTemplateRowModel,
    TemplateDamageDistributionModel,
    TemplateModel,
)
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.output_method import QTemplateTabOutputMethodTable
from ww.ui.table import QUneditableTable


class QTemplateDamageDistributionUneditableTable(QUneditableTable):
    def __init__(self, data: List[List[str]], column_names: List[str]):
        super().__init__(data, column_names)

    def _init_column_width(self):
        for _, col_index in self.column_names_table.items():
            self.setColumnWidth(col_index, 200)

    def reset_data(self):
        self.setRowCount(0)
        self.setRowCount(3)
        self.data = self.get_empty_data(row_count=3)
        self._init_cells()


def get_row(
    resonator_name: str,
    damage_distribution: TemplateDamageDistributionModel,
    enum_class: Enum,
) -> List[str]:
    column_length = len(enum_class) + 2
    row = ["" for _ in range(column_length)]
    resonator = damage_distribution.resonators.get(resonator_name, None)
    if resonator is None:
        return row

    resonator_total_damage = resonator.damage
    row[0] = resonator_name
    for i, e in enumerate(enum_class):
        resonator_damage_str = resonator.get_damage_string_with_percentage(
            e.name.lower()
        )
        row[i + 1] = resonator_damage_str

    damage_total_resonators = damage_distribution.damage
    resonator_total_damage_percentage = resonator_total_damage / damage_total_resonators
    resonator_total_damage_str = (
        f"{resonator_total_damage:,.2f} ({resonator_total_damage_percentage:.2%})"
    )
    row[-1] = resonator_total_damage_str

    return row


class QTemplateDamageDistributionTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_analyze_btn = QPushButton(_(ZhTwEnum.ANALYZE))
        self.q_analyze_btn.setFixedHeight(40)
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_analyze_btn)

        self.skill_type_column_names = (
            [_(ZhTwEnum.NAME)]
            + [e.value for e in SkillBonusTypeEnum]
            + [_(ZhTwEnum.TOTAL_DAMAGE)]
        )

        self.q_skill_type_table = QTemplateDamageDistributionUneditableTable(
            [["" for _ in range(len(self.skill_type_column_names))] for _ in range(3)],
            self.skill_type_column_names,
        )

        self.skill_column_names = (
            [_(ZhTwEnum.NAME)]
            + [e.value for e in ResonatorSkillTypeEnum]
            + [_(ZhTwEnum.TOTAL_DAMAGE)]
        )

        self.q_skill_table = QTemplateDamageDistributionUneditableTable(
            [["" for _ in range(len(self.skill_column_names))] for _ in range(3)],
            self.skill_column_names,
        )

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_skill_type_table)
        self.layout.addWidget(self.q_skill_table)

        self.setLayout(self.layout)

    def analyze(self):
        self.q_template_basic_tab: QTemplateBasicTab = self._parent.q_template_basic_tab
        self.q_output_method_table: QTemplateTabOutputMethodTable = (
            self._parent.q_template_output_method_tab.q_output_method_table
        )

        calculated_rows: List[CalculatedTemplateRowModel] = (
            self.q_output_method_table.calculated_rows
        )
        template: TemplateModel = self._parent.get_template()

        test_resonator_id_1 = template.test_resonator_id_1
        test_resonator_id_2 = template.test_resonator_id_2
        test_resonator_id_3 = template.test_resonator_id_3

        test_resonators = self.q_template_basic_tab.get_test_resonators()
        test_resonator_names = ["", "", ""]
        if not test_resonators:
            prefix = _(ZhTwEnum.ECHOES_THEORY_1)
            template: TemplateModel = self.q_template_basic_tab.get_template()

            simulated_resonators = SimulatedResonators(template)
            resonators_table = simulated_resonators.get_3_resonators_with_prefix(prefix)

            calculated_resonators = simulated_resonators.get_calculated_resonators(
                resonators_table
            )
            calculated_resonators_table = calculated_resonators.get_table()
            id_to_name = calculated_resonators.get_id_to_name()
            test_resonators = OrderedDict()
            for id, name in id_to_name.items():
                test_resonators[name] = id

            if len(test_resonators) == 0:
                return

            damage = Damage(
                monster_id=template.monster_id,
                resonators_table=resonators_table,
                calculated_resonators_table=calculated_resonators_table,
            )

            resonator_names = test_resonators.keys()
            for i, resonator_name in enumerate(resonator_names):
                if i > 2:
                    break
                test_resonator_names[i] = resonator_name

        else:
            damage = Damage(monster_id=template.monster_id)

            for test_resonator_name, test_resonator_id in test_resonators.items():
                if test_resonator_id == test_resonator_id_1:
                    test_resonator_names[0] = test_resonator_name
                elif test_resonator_id == test_resonator_id_2:
                    test_resonator_names[1] = test_resonator_name
                elif test_resonator_id == test_resonator_id_3:
                    test_resonator_names[2] = test_resonator_name

        # Calculate
        damage_distribution = damage.extract_damage_distribution_from_rows(
            test_resonators, template.id, template.monster_id, calculated_rows
        )

        # Create table data
        skill_type_data = []
        skill_data = []
        for resonator_name in test_resonator_names:
            skill_type_row = get_row(
                resonator_name, damage_distribution, SkillBonusTypeEnum
            )
            skill_type_data.append(skill_type_row)

            skill_row = get_row(
                resonator_name, damage_distribution, ResonatorSkillTypeEnum
            )
            skill_data.append(skill_row)

        self.q_skill_type_table.load_list(skill_type_data)
        self.q_skill_table.load_list(skill_data)

    def reset_data(self):
        self.q_skill_type_table.reset_data()
        self.q_skill_table.reset_data()
