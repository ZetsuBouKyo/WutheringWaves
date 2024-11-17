from functools import partial
from typing import Dict, List

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import Damage
from ww.html.template import (
    export_echo_as_png,
    export_html_template_output_methods_as_png,
    export_html_template_resonator_model_as_png,
    export_resonator_skill_bonus_type_damage_distribution_as_png,
    export_team_damage_distribution_as_png,
)
from ww.locale import ZhTwEnum, _
from ww.model.template import CalculatedTemplateRowModel, TemplateModel
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.label import QTemplateLabelTab
from ww.ui.developer.template.output_method import (
    QTemplateOutputMethodTab,
    QTemplateTabOutputMethodTable,
)


class QTemplateExportTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self.q_template_label_tab: QTemplateLabelTab = self._parent.q_template_label_tab
        self.q_template_basic_tab: QTemplateBasicTab = self._parent.q_template_basic_tab
        self.q_template_output_method_tab: QTemplateOutputMethodTab = (
            self._parent.q_template_output_method_tab
        )

        self.layout = QVBoxLayout()
        self._btn_height = 40
        self._btn_width = 200

        # All
        self.q_btns_layout = QHBoxLayout()
        self.q_export_all_images_btn = QPushButton(_(ZhTwEnum.EXPORT_ALL_IMAGES))
        self.q_export_all_images_btn.clicked.connect(self.export_all_images)
        self.q_export_all_images_btn.setFixedWidth(self._btn_width)
        self.q_export_all_images_btn.setFixedHeight(self._btn_height)
        self.q_btns_layout.addWidget(self.q_export_all_images_btn)
        self.q_btns_layout.addStretch()

        self.layout.addLayout(self.q_btns_layout)

        # Resonator
        self.q_btns_2_layout = QHBoxLayout()
        self.q_export_resonator_images_btn = QPushButton(
            _(ZhTwEnum.EXPORT_RESONATOR_IMAGES)
        )
        self.q_export_resonator_images_btn.clicked.connect(
            partial(self.export_resonator_images, True)
        )
        self.q_export_resonator_images_btn.setFixedWidth(self._btn_width)
        self.q_export_resonator_images_btn.setFixedHeight(self._btn_height)
        self.q_btns_2_layout.addWidget(self.q_export_resonator_images_btn)
        self.q_btns_2_layout.addStretch()

        self.layout.addLayout(self.q_btns_2_layout)

        # Output methods
        self.init_output_method(self.layout)

        # Damage distribution
        self.init_damage_distribution(self.layout)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def init_output_method(self, parent_layout: QVBoxLayout):
        layout = QHBoxLayout()
        suffix_label = QLabel(_(ZhTwEnum.LABEL))
        suffix_label.setFixedWidth(60)
        suffix_label.setFixedHeight(40)
        suffix_combobox = QAutoCompleteComboBox(
            getOptions=self.q_template_label_tab.get_label_names
        )
        suffix_combobox.setFixedWidth(120)
        suffix_combobox.setFixedHeight(40)

        # Height
        height_label = QLabel(_(ZhTwEnum.EXPORT_IMAGE_HEIGHT))
        height_label.setToolTip(_(ZhTwEnum.TOOL_TIP_OUTPUT_METHOD_PNG_HEIGHT))
        height_label.setFixedWidth(120)
        height_label.setFixedHeight(40)
        height_line = QLineEdit("")
        height_line.setToolTip(_(ZhTwEnum.TOOL_TIP_OUTPUT_METHOD_PNG_HEIGHT))
        height_line.setFixedWidth(200)
        height_line.setFixedHeight(40)

        # Button
        btn = QPushButton(_(ZhTwEnum.EXPORT_OUTPUT_METHOD_IMAGES))
        btn.clicked.connect(partial(self.export_output_method_images, True))
        btn.setFixedWidth(self._btn_width)
        btn.setFixedHeight(self._btn_height)

        layout.addWidget(btn)
        layout.addWidget(suffix_label)
        layout.addWidget(suffix_combobox)
        layout.addWidget(height_label)
        layout.addWidget(height_line)
        layout.addStretch()

        parent_layout.addLayout(layout)

        self.q_output_method_height_line = height_line
        self.q_output_method_label_combobox = suffix_combobox

    def init_damage_distribution(self, parent_layout: QVBoxLayout):
        layout = QHBoxLayout()
        btn = QPushButton(_(ZhTwEnum.EXPORT_DAMAGE_DISTRIBUTION_IMAGES))
        btn.clicked.connect(partial(self.export_damage_distribution, True))
        btn.setFixedWidth(self._btn_width)
        btn.setFixedHeight(self._btn_height)

        suffix_label = QLabel(_(ZhTwEnum.LABEL))
        suffix_label.setFixedWidth(60)
        suffix_label.setFixedHeight(40)
        suffix_combobox = QAutoCompleteComboBox(
            getOptions=self.q_template_label_tab.get_label_names
        )
        suffix_combobox.setFixedWidth(120)
        suffix_combobox.setFixedHeight(40)

        layout.addWidget(btn)
        layout.addWidget(suffix_label)
        layout.addWidget(suffix_combobox)
        layout.addStretch()

        parent_layout.addLayout(layout)

        self.q_damage_distribution_combobox = suffix_combobox

    def export_resonator_images(self, is_progress: bool = False):
        template: TemplateModel = self._parent.get_template()

        export_html_template_resonator_model_as_png(
            template.id, template.test_resonator_id_1
        )
        export_html_template_resonator_model_as_png(
            template.id, template.test_resonator_id_2
        )
        export_html_template_resonator_model_as_png(
            template.id, template.test_resonator_id_3
        )

        test_resonators: Dict[str, str] = (
            self.q_template_basic_tab.get_test_resonators()
        )
        for resonator_id in test_resonators.values():
            export_echo_as_png(template.id, resonator_id)

        if is_progress:
            self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def export_output_method_images(self, is_progress: bool = False):
        template: TemplateModel = self._parent.get_template()

        # Label
        label = self.q_output_method_label_combobox.currentText()
        if label.strip() == "":
            labels = None
        else:
            labels = [label]

        # Height
        output_methods_height = self.q_output_method_height_line.text()

        if output_methods_height:
            try:
                output_methods_height = int(output_methods_height)
                export_html_template_output_methods_as_png(
                    template.id, template.rows, output_methods_height, labels=labels
                )
            except ValueError:
                export_html_template_output_methods_as_png(
                    template.id, template.rows, labels=labels
                )
        if is_progress:
            self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def export_damage_distribution(self, is_progress: bool = False):
        template: TemplateModel = self._parent.get_template()

        # Calculated rows
        q_output_method_table: QTemplateTabOutputMethodTable = (
            self.q_template_output_method_tab.q_output_method_table
        )
        calculated_rows: List[CalculatedTemplateRowModel] = (
            q_output_method_table.calculated_rows
        )

        # Resonators
        test_resonators: Dict[str, str] = (
            self.q_template_basic_tab.get_test_resonators()
        )

        # Label
        label = self.q_damage_distribution_combobox.currentText()
        if label.strip() == "":
            labels = None
        else:
            labels = [label]

        damage = Damage(monster_id=template.monster_id)
        damage_distributions = (
            damage.extract_damage_distributions_from_rows_with_labels(
                test_resonators,
                template.id,
                template.monster_id,
                calculated_rows,
                labels=labels,
            )
        )
        for label_name, damage_distribution in damage_distributions.items():
            export_team_damage_distribution_as_png(
                test_resonators.keys(), damage_distribution, suffix=label_name
            )
            for resonator_name in damage_distribution.resonators.keys():
                export_resonator_skill_bonus_type_damage_distribution_as_png(
                    resonator_name, damage_distribution, suffix=label_name
                )

        if is_progress:
            self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def export_all_images(self):
        self.export_resonator_images()
        self.export_output_method_images()
        self.export_damage_distribution()

        self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def reset_data(self):
        self.q_output_method_height_line.setText("")
        self.q_output_method_label_combobox.setCurrentText("")
        self.q_damage_distribution_combobox.setCurrentText("")
