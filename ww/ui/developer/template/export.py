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
    export_damage_distribution_as_png,
    export_html_template_output_method_model_as_png,
    export_html_template_resonator_model_as_png,
)
from ww.locale import ZhTwEnum, _
from ww.model.template import CalculatedTemplateRowModel, TemplateModel
from ww.ui.developer.template.output_method import QTemplateTabOutputMethodTable


class QTemplateExportTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.layout = QVBoxLayout()

        # Buttons
        self.q_btns_layout = QHBoxLayout()
        self.q_export_image_btn = QPushButton(_(ZhTwEnum.EXPORT_IMAGE))
        self.q_export_image_btn.clicked.connect(self.export_images)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_export_image_btn)

        self.layout.addLayout(self.q_btns_layout)

        self.q_output_method_line = self.set_line(
            self.layout,
            _(ZhTwEnum.OUTPUT_METHOD),
            _(ZhTwEnum.TOOL_TIP_OUTPUT_METHOD_PNG_HEIGHT),
        )

        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_line(
        self, parent_layout: QVBoxLayout, label_name: str, tool_tip: str
    ) -> QLineEdit:
        layout = QHBoxLayout()
        label = QLabel(label_name)
        label.setToolTip(tool_tip)
        label.setFixedWidth(150)
        label.setFixedHeight(40)
        line = QLineEdit("")
        line.setToolTip(tool_tip)
        line.setFixedWidth(400)
        line.setFixedHeight(40)

        layout.addWidget(label)
        layout.addWidget(line)
        layout.addStretch()

        parent_layout.addLayout(layout)
        return line

    def export_images(self):
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

        output_methods_height = self.q_output_method_line.text()
        if output_methods_height:
            try:
                output_methods_height = int(output_methods_height)
                export_html_template_output_method_model_as_png(
                    template.id, template.rows, output_methods_height
                )
            except ValueError:
                export_html_template_output_method_model_as_png(
                    template.id, template.rows
                )

        # Damage distribution
        q_output_method_table: QTemplateTabOutputMethodTable = (
            self._parent.q_template_output_method_tab.q_output_method_table
        )

        calculated_rows: List[CalculatedTemplateRowModel] = (
            q_output_method_table.calculated_rows
        )

        test_resonators: Dict[str, str] = (
            self._parent.q_template_basic_tab.get_test_resonators()
        )
        damage = Damage(monster_id=template.monster_id)
        damage_distribution = damage.extract_damage_distribution_from_rows(
            test_resonators, template.id, template.monster_id, calculated_rows
        )
        export_damage_distribution_as_png(damage_distribution)

        self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))
