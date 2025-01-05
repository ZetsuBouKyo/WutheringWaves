from pathlib import Path

from PySide2.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.crud.template import (
    TEMPLATE_HOME_PATH,
    delete_template,
    get_template,
    save_template,
)
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateModel, TemplateRowModel
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.damage_distribution import QTemplateDamageDistributionTab
from ww.ui.developer.template.export import QTemplateExportTab
from ww.ui.developer.template.help import QTemplateHelpTab
from ww.ui.developer.template.label import QTemplateLabelTab
from ww.ui.developer.template.output_method import QTemplateOutputMethodTab
from ww.ui.progress_bar import QHProgressBar


class QTemplateTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()

        self.q_new_btn = QPushButton(_(ZhTwEnum.NEW))
        self.q_new_btn.clicked.connect(self.new)
        self.q_save_btn = QPushButton(_(ZhTwEnum.SAVE))
        self.q_save_btn.clicked.connect(self.save)
        self.q_load_btn = QPushButton(_(ZhTwEnum.LOAD))
        self.q_load_btn.setToolTip(_(ZhTwEnum.LOAD_SELECTED_TEMPLATE_ID))
        self.q_load_btn.clicked.connect(self.load)
        self.q_delete_btn = QPushButton(_(ZhTwEnum.DELETE))
        self.q_delete_btn.setToolTip(_(ZhTwEnum.DELETE_SELECTED_TEMPLATE_ID))
        self.q_delete_btn.clicked.connect(self.delete)

        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_new_btn)
        self.q_btns_layout.addWidget(self.q_save_btn)
        self.q_btns_layout.addWidget(self.q_load_btn)
        self.q_btns_layout.addWidget(self.q_delete_btn)

        # Progress bar
        self.q_progress_bar = QHProgressBar()

        # Tabs
        self.q_tabs = QTabWidget()

        # Basic
        self.q_template_basic_tab = QTemplateBasicTab()

        # Label
        self.q_template_label_tab = QTemplateLabelTab()

        # Output method
        self.q_template_output_method_tab = QTemplateOutputMethodTab(
            self, self.q_progress_bar
        )

        # Damage analysis
        self.q_template_damage_distribution = QTemplateDamageDistributionTab(self)

        # Export
        self.q_template_export = QTemplateExportTab(self)

        # Help
        self.q_template_help_tab = QTemplateHelpTab()

        self.q_tabs.addTab(self.q_template_basic_tab, _(ZhTwEnum.TAB_BASIC))
        self.q_tabs.addTab(self.q_template_label_tab, _(ZhTwEnum.TAB_LABEL))
        self.q_tabs.addTab(
            self.q_template_output_method_tab, _(ZhTwEnum.TAB_OUTPUT_METHOD)
        )
        self.q_tabs.addTab(
            self.q_template_damage_distribution, _(ZhTwEnum.TAB_DAMAGE_DISTRIBUTION)
        )
        self.q_tabs.addTab(self.q_template_export, _(ZhTwEnum.TAB_EXPORT))
        self.q_tabs.addTab(self.q_template_help_tab, _(ZhTwEnum.TAB_HELP))

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_tabs)
        self.layout.addWidget(self.q_progress_bar)
        self.setLayout(self.layout)

    def get_template(self) -> TemplateModel:
        template = self.q_template_basic_tab.get_template()
        labels = self.q_template_label_tab.get_labels()
        rows = self.q_template_output_method_tab.get_rows()
        template.labels = labels
        template.rows = rows

        return template

    def new(self):
        self.q_template_basic_tab.reset_data()
        self.q_template_label_tab.reset_data()
        self.q_template_output_method_tab.reset_data()
        self.q_template_damage_distribution.reset_data()
        self.q_template_export.reset_data()

    def save(self):
        self.q_progress_bar.set(0.0, _(ZhTwEnum.SAVING))

        template = self.get_template()
        if template.id == "":
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.ID_MUST_NOT_EMPTY)
            )
            return
        template_fname = f"{template.id}.json"
        template_path = Path(TEMPLATE_HOME_PATH) / template_fname

        self.q_progress_bar.set_percentage(10.0)

        if template_path.exists():
            confirmation = QMessageBox.question(
                self,
                _(ZhTwEnum.FILE_EXISTS),
                f"{_(ZhTwEnum.FILE_OVERWRITE_OR_NOT)}'{template_fname}'?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirmation == QMessageBox.No:
                self.q_progress_bar.reset()
                return

        self.q_progress_bar.set_percentage(20.0)

        save_template(template.id, template)

        self.q_progress_bar.set(100.0, _(ZhTwEnum.SAVED))

    def load(self):
        template_id = self.q_template_basic_tab.get_template_id()
        if not template_id:
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.TO_SELECT_TEMPLATE_ID)
            )
            return

        template = get_template(template_id)

        if template is None:
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.TO_SELECT_TEMPLATE_ID)
            )
            return

        confirmation = QMessageBox.question(
            self,
            _(ZhTwEnum.FILE),
            _(ZhTwEnum.CONFIRM_LOAD),
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.No:
            return

        self.q_progress_bar.set(0.0, _(ZhTwEnum.LOADING))

        if len(template.rows) == 0:
            template.rows.append(TemplateRowModel())

        self.q_progress_bar.set_percentage(20.0)
        self.q_template_basic_tab.load(template)

        self.q_progress_bar.set_percentage(60.0)
        self.q_template_label_tab.load(template.labels)
        self.q_template_output_method_tab.load(template.rows)

        self.q_progress_bar.set(100.0, _(ZhTwEnum.LOADED))

    def delete(self):
        template_id = self.q_template_basic_tab.get_template_id()
        if not template_id:
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                _(ZhTwEnum.TO_SELECT_ID_TO_DELETE),
            )
            return

        self.q_progress_bar.reset()

        confirmation = QMessageBox.question(
            self,
            _(ZhTwEnum.DELETE),
            f"{_(ZhTwEnum.CONFIRM_DELETE_FILE)} '{template_id}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.No:
            return

        if delete_template(template_id):
            self.q_template_basic_tab.reset_template_id()
