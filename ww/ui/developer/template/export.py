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
    export_damage_distribution_as_png,
    export_echo_as_png,
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
        self._btn_height = 40
        self._btn_width = 200

        # All
        self.q_btns_layout = QHBoxLayout()
        self.q_export_all_images_btn = QPushButton(_(ZhTwEnum.EXPORT_ALL_IMAGES))
        self.q_export_all_images_btn.clicked.connect(self.export_all_images)
        self.q_export_all_images_btn.setFixedWidth(self._btn_width)
        self.q_export_all_images_btn.setFixedHeight(self._btn_height)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_export_all_images_btn)

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
        self.q_btns_2_layout.addStretch()
        self.q_btns_2_layout.addWidget(self.q_export_resonator_images_btn)

        self.layout.addLayout(self.q_btns_2_layout)

        # Output methods
        self.q_output_method_line = self.init_output_method(
            self.layout,
            _(ZhTwEnum.OUTPUT_METHOD),
            _(ZhTwEnum.TOOL_TIP_OUTPUT_METHOD_PNG_HEIGHT),
        )

        # Damage distribution
        self.q_btns_3_layout = QHBoxLayout()
        self.q_export_dmg_dist_images_btn = QPushButton(
            _(ZhTwEnum.EXPORT_DAMAGE_DISTRIBUTION_IMAGES)
        )
        self.q_export_dmg_dist_images_btn.clicked.connect(
            partial(self.export_damage_distribution, True)
        )
        self.q_export_dmg_dist_images_btn.setFixedWidth(self._btn_width)
        self.q_export_dmg_dist_images_btn.setFixedHeight(self._btn_height)
        self.q_btns_3_layout.addStretch()
        self.q_btns_3_layout.addWidget(self.q_export_dmg_dist_images_btn)

        self.layout.addLayout(self.q_btns_3_layout)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def init_output_method(
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

        btn = QPushButton(_(ZhTwEnum.EXPORT_OUTPUT_METHOD_IMAGES))
        btn.clicked.connect(partial(self.export_output_method_images, True))
        btn.setFixedWidth(self._btn_width)
        btn.setFixedHeight(self._btn_height)

        layout.addWidget(btn)

        parent_layout.addLayout(layout)
        return line

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
            self._parent.q_template_basic_tab.get_test_resonators()
        )
        for resonator_id in test_resonators.values():
            export_echo_as_png(template.id, resonator_id)

        if is_progress:
            self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def export_output_method_images(self, is_progress: bool = False):
        template: TemplateModel = self._parent.get_template()
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
        if is_progress:
            self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def export_damage_distribution(self, is_progress: bool = False):
        template: TemplateModel = self._parent.get_template()

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
        export_damage_distribution_as_png(test_resonators.keys(), damage_distribution)

        if is_progress:
            self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))

    def export_all_images(self):
        self.export_resonator_images()
        self.export_output_method_images()
        self.export_damage_distribution()

        self._parent.q_progress_bar.set_message(_(ZhTwEnum.IMAGE_EXPORT_SUCCESSFUL))
