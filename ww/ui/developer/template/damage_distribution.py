from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.locale import ZhHantEnum, _
from ww.model.template import CalculatedTemplateRowModel, TemplateModel
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.output_method import QTemplateTabOutputMethodTable


class QTemplateDamageDistributionSubTab(QWidget):
    def __init__(self):
        super().__init__()

    def analyze(
        self, resonator_name: str, calculated_rows: List[CalculatedTemplateRowModel]
    ): ...


class QTemplateDamageDistributionSubTabs(QTabWidget):
    def __init__(self, template_tabs):
        super().__init__()
        self.q_template_tabs = template_tabs

        self.q_resonator_1 = QTemplateDamageDistributionSubTab()
        self.q_resonator_2 = QTemplateDamageDistributionSubTab()
        self.q_resonator_3 = QTemplateDamageDistributionSubTab()

        self.addTab(self.q_resonator_1, _(ZhHantEnum.RESONATOR_1))
        self.addTab(self.q_resonator_2, _(ZhHantEnum.RESONATOR_2))
        self.addTab(self.q_resonator_3, _(ZhHantEnum.RESONATOR_3))

    def analyze(self, template: TemplateModel):
        tab_text_1 = _(ZhHantEnum.RESONATOR_1)
        tab_text_2 = _(ZhHantEnum.RESONATOR_2)
        tab_text_3 = _(ZhHantEnum.RESONATOR_3)

        self.q_template_basic_tab: QTemplateBasicTab = (
            self.q_template_tabs.q_template_basic_tab
        )
        self.q_output_method_table: QTemplateTabOutputMethodTable = (
            self.q_template_tabs.q_template_output_method_tab.q_output_method_table
        )

        test_resonators = self.q_template_basic_tab.get_test_resonators()

        test_resonator_id_1 = template.test_resonator_id_1
        test_resonator_id_2 = template.test_resonator_id_2
        test_resonator_id_3 = template.test_resonator_id_3

        for test_resonator_name, test_resonator_id in test_resonators.items():
            if test_resonator_id == test_resonator_id_1:
                tab_text_1 = test_resonator_name
            elif test_resonator_id == test_resonator_id_2:
                tab_text_2 = test_resonator_name
            elif test_resonator_id == test_resonator_id_3:
                tab_text_3 = test_resonator_name

        self.setTabText(0, tab_text_1)
        self.setTabText(1, tab_text_2)
        self.setTabText(2, tab_text_3)

        calculated_rows: List[CalculatedTemplateRowModel] = (
            self.q_output_method_table.calculated_rows
        )


class QTemplateDamageDistributionTab(QWidget):
    def __init__(self, template_tabs):
        super().__init__()
        self.q_template_tabs = template_tabs

        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_analyze_btn = QPushButton(_(ZhHantEnum.ANALYZE))
        self.q_analyze_btn.setFixedHeight(40)
        self.q_analyze_btn.clicked.connect(self.analyze)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_analyze_btn)

        self.q_sub_tabs = QTemplateDamageDistributionSubTabs(self.q_template_tabs)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_sub_tabs)

        self.setLayout(self.layout)

    def analyze(self):
        template: TemplateModel = self.q_template_tabs.get_template()
        self.q_sub_tabs.analyze(template)
