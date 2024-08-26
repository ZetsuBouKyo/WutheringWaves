from typing import List

from PySide2.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ww.calc.damage import Damage
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
        damage = Damage(monster_id=template.monster_id)
        damage_distribution = damage.extract_damage_distribution_from_rows(
            test_resonators, template.id, template.monster_id, calculated_rows
        )

        # Create table data

        data = []
        damage_total_resonators = damage_distribution.damage
        for resonator_name in test_resonator_names:
            row = ["" for _ in range(len(self.column_names))]
            resonator = damage_distribution.resonators.get(resonator_name, None)
            if resonator is None:
                data.append(row)
                continue

            resonator_total_damage = resonator.damage
            row[0] = resonator_name
            for i, e in enumerate(SkillBonusTypeEnum):
                resonator_damage_str = resonator.get_damage_string_with_percentage(
                    e.name.lower()
                )
                row[i + 1] = resonator_damage_str

            resonator_total_damage_percentage = (
                resonator_total_damage / damage_total_resonators
            )
            resonator_total_damage_str = f"{resonator_total_damage:,.2f} ({resonator_total_damage_percentage:.2%})"
            row[-1] = resonator_total_damage_str
            data.append(row)

        self.q_table.load_list(data)
