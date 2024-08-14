from decimal import Decimal
from typing import Dict, List

from PySide2.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.model.template import CalculatedTemplateRowModel, TemplateModel
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.output_method import QTemplateTabOutputMethodTable
from ww.ui.table import QUneditableTable


class QTemplateDamageDistributionUneditableTable(QUneditableTable):
    def __init__(self, data: List[List[str]], column_names: List[str]):
        super().__init__(data, column_names)

    def _init_column_width(self):
        for _, col_index in self.column_names_table.items():
            self.setColumnWidth(col_index, 200)


class QTemplateDamageDistributionTab(QWidget):
    def __init__(self, template_tabs):
        super().__init__()
        self.q_template_tabs = template_tabs

        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_analyze_btn = QPushButton(_(ZhTwEnum.ANALYZE))
        self.q_analyze_btn.setFixedHeight(40)
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_analyze_btn)

        self.column_names = (
            [_(ZhTwEnum.NAME)]
            + [e.value for e in SkillBonusTypeEnum]
            + [_(ZhTwEnum.TOTAL_DAMAGE)]
        )
        self.q_table = QTemplateDamageDistributionUneditableTable(
            [["" for _ in range(len(self.column_names))] for _ in range(3)],
            self.column_names,
        )

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_table)

        self.setLayout(self.layout)

    def analyze(self):
        self.q_template_basic_tab: QTemplateBasicTab = (
            self.q_template_tabs.q_template_basic_tab
        )
        self.q_output_method_table: QTemplateTabOutputMethodTable = (
            self.q_template_tabs.q_template_output_method_tab.q_output_method_table
        )

        calculated_rows: List[CalculatedTemplateRowModel] = (
            self.q_output_method_table.calculated_rows
        )
        template: TemplateModel = self.q_template_tabs.get_template()

        test_resonator_id_1 = template.test_resonator_id_1
        test_resonator_id_2 = template.test_resonator_id_2
        test_resonator_id_3 = template.test_resonator_id_3

        test_resonator_names = ["", "", ""]

        test_resonators = self.q_template_basic_tab.get_test_resonators()
        for test_resonator_name, test_resonator_id in test_resonators.items():
            if test_resonator_id == test_resonator_id_1:
                test_resonator_names[0] = test_resonator_name
            elif test_resonator_id == test_resonator_id_2:
                test_resonator_names[1] = test_resonator_name
            elif test_resonator_id == test_resonator_id_3:
                test_resonator_names[2] = test_resonator_name

        # Calculate
        damage_total_resonators = Decimal("0.0")
        damage_total: Dict[str, Decimal] = {}
        damage_distribution: Dict[str, Dict[SkillBonusTypeEnum, Decimal]] = {}
        for calculated_row in calculated_rows:
            resonator_name = calculated_row.resonator_name
            resonator = damage_distribution.get(resonator_name, None)
            if resonator is None:
                damage_total[resonator_name] = Decimal("0.0")
                damage_distribution[resonator_name] = {
                    e.value: Decimal("0.0") for e in SkillBonusTypeEnum
                }

            resonator_skill_type_bonus = calculated_row.resonator_skill_type_bonus
            if (
                damage_distribution.get(resonator_name, {}).get(
                    resonator_skill_type_bonus, None
                )
                is None
            ):
                resonator_skill_type_bonus = SkillBonusTypeEnum.NONE.value

            damage_distribution[resonator_name][
                resonator_skill_type_bonus
            ] += calculated_row.damage
            damage_total[resonator_name] += calculated_row.damage
            damage_total_resonators += calculated_row.damage

        # Create table data

        data = []
        for resonator_name in test_resonator_names:
            row = ["" for _ in range(len(self.column_names))]
            resonator = damage_distribution.get(resonator_name, None)
            if resonator is None:
                data.append(row)
                continue

            resonator_total_damage = damage_total[resonator_name]
            row[0] = resonator_name
            for i, e in enumerate(SkillBonusTypeEnum):
                resonator_skill_type_bonus = e.value
                resonator_damage = resonator[resonator_skill_type_bonus]
                resonator_damage_percentage = resonator_damage / resonator_total_damage
                resonator_damage_str = (
                    f"{resonator_damage:.2f} ({resonator_damage_percentage:.2%})"
                )
                row[i + 1] = resonator_damage_str

            resonator_total_damage_percentage = (
                resonator_total_damage / damage_total_resonators
            )
            resonator_total_damage_str = f"{resonator_total_damage:.2f} ({resonator_total_damage_percentage:.2%})"
            row[-1] = resonator_total_damage_str
            data.append(row)

        self.q_table.load_list(data)
