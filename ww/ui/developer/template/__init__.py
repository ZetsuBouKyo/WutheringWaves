from pathlib import Path

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.crud.template import (
    TEMPLATE_HOME_PATH,
    get_template,
    get_template_path,
    save_template,
)
from ww.locale import ZhTwEnum, _
from ww.model.echo import EchoTsvColumnEnum
from ww.model.template import (
    TemplateHtmlResonatorModel,
    TemplateModel,
    TemplateRowModel,
)
from ww.tables.echo import EchoListTable
from ww.tables.resonator import CalculatedResonatorsTable, ResonatorsTable
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.damage_distribution import QTemplateDamageDistributionTab
from ww.ui.developer.template.help import QTemplateHelpTab
from ww.ui.developer.template.output_method import QTemplateOutputMethodTab
from ww.ui.progress_bar import QHProgressBar

echo_list_table = EchoListTable()
echo_list = [
    row[EchoTsvColumnEnum.PRIMARY_KEY] for _, row in echo_list_table.df.iterrows()
]


def get_template_html_resonator_model(resonator_id: str) -> TemplateHtmlResonatorModel:
    if not resonator_id:
        return
    calculated_resonators_table = CalculatedResonatorsTable()
    calculated_resonator = calculated_resonators_table.get_calculated_resonator_model(
        resonator_id
    )
    if calculated_resonator is None:
        return

    resonators_table = ResonatorsTable()
    resonator = resonators_table.get_row(resonator_id)
    if resonator is None:
        return

    template_html_model = TemplateHtmlResonatorModel(
        name="",
        chain="",
        element="",
        weapon_name="",
        weapon_rank="",
        weapon_level="",
        level="",
        hp=calculated_resonator.calculated_hp,
        attack=calculated_resonator.calculated_atk,
        defense=calculated_resonator.calculated_def,
        crit_rate=calculated_resonator.calculated_crit_rate,
        crit_dmg=calculated_resonator.calculated_crit_dmg,
        energy_regen=calculated_resonator.calculated_energy_regen,
        resonance_skill_dmg_bonus=calculated_resonator.calculated_resonance_skill_dmg_bonus,
        basic_attack_dmg_bonus=calculated_resonator.calculated_basic_attack_dmg_bonus,
        heavy_attack_dmg_bonus=calculated_resonator.calculated_heavy_attack_dmg_bonus,
        resonance_liberation_dmg_bonus=calculated_resonator.calculated_resonance_liberation_dmg_bonus,
        healing_bonus=calculated_resonator.calculated_healing_bonus,
        physical_dmg_bonus=calculated_resonator.calculated_physical_dmg_bonus,
        glacio_dmg_bonus=calculated_resonator.calculated_glacio_dmg_bonus,
        fusion_dmg_bonus=calculated_resonator.calculated_fusion_dmg_bonus,
        electro_dmg_bonus=calculated_resonator.calculated_electro_dmg_bonus,
        aero_dmg_bonus=calculated_resonator.calculated_aero_dmg_bonus,
        spectro_dmg_bonus=calculated_resonator.calculated_spectro_dmg_bonus,
        havoc_dmg_bonus=calculated_resonator.calculated_havoc_dmg_bonus,
        physical_dmg_res=calculated_resonator.calculated_physical_dmg_res,
        glacio_dmg_res=calculated_resonator.calculated_glacio_dmg_res,
        fusion_dmg_res=calculated_resonator.calculated_fusion_dmg_res,
        electro_dmg_res=calculated_resonator.calculated_electro_dmg_res,
        aero_dmg_res=calculated_resonator.calculated_aero_dmg_res,
        spectro_dmg_res=calculated_resonator.calculated_spectro_dmg_res,
        havoc_dmg_res=calculated_resonator.calculated_havoc_dmg_res,
        normal_attack_lv="",
        resonance_skill_lv="",
        resonance_liberation_lv="",
        forte_circuit_lv="",
        inherent_skill_1="",
        inherent_skill_2="",
        resonator_src="",
        element_class_name="",
        element_src="",
    )
    print(template_html_model)


class QTemplateTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()

        self.q_export_image_btn = QPushButton(_(ZhTwEnum.EXPORT_IMAGE))
        self.q_export_image_btn.clicked.connect(self.export_images)
        self.q_save_btn = QPushButton(_(ZhTwEnum.SAVE))
        self.q_save_btn.clicked.connect(self.save)
        self.q_load_btn = QPushButton(_(ZhTwEnum.LOAD))
        self.q_load_btn.setToolTip(_(ZhTwEnum.LOAD_SELECTED_TEMPLATE_ID))
        self.q_load_btn.clicked.connect(self.load)
        self.q_delete_btn = QPushButton(_(ZhTwEnum.DELETE))
        self.q_delete_btn.setToolTip(_(ZhTwEnum.DELETE_SELECTED_TEMPLATE_ID))
        self.q_delete_btn.clicked.connect(self.delete)

        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_export_image_btn)
        self.q_btns_layout.addWidget(self.q_save_btn)
        self.q_btns_layout.addWidget(self.q_load_btn)
        self.q_btns_layout.addWidget(self.q_delete_btn)

        # Progress bar
        self.q_progress_bar = QHProgressBar()

        # Tabs
        self.q_tabs = QTabWidget()

        # Basic
        self.q_template_basic_tab = QTemplateBasicTab()
        # Output method
        self.q_template_output_method_tab = QTemplateOutputMethodTab(
            self.q_template_basic_tab, self.q_progress_bar
        )
        # Damage analysis
        self.q_template_damage_distribution = QTemplateDamageDistributionTab(self)
        # Help
        self.q_template_help_tab = QTemplateHelpTab()

        self.q_tabs.addTab(self.q_template_basic_tab, _(ZhTwEnum.TAB_BASIC))
        self.q_tabs.addTab(
            self.q_template_output_method_tab, _(ZhTwEnum.TAB_OUTPUT_METHOD)
        )
        self.q_tabs.addTab(
            self.q_template_damage_distribution, _(ZhTwEnum.TAB_DAMAGE_DISTRIBUTION)
        )
        self.q_tabs.addTab(self.q_template_help_tab, _(ZhTwEnum.TAB_HELP))

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_tabs)
        self.layout.addWidget(self.q_progress_bar)
        self.setLayout(self.layout)

    def get_template(self) -> TemplateModel:
        template_id = self.q_template_basic_tab.get_template_id()
        template_id = template_id.strip()

        test_resonator_ids = self.q_template_basic_tab.get_test_resonator_ids()
        monster_id = self.q_template_basic_tab.get_monster_id()
        description = self.q_template_basic_tab.get_description()
        resonators = self.q_template_basic_tab.get_resonators()
        rows = self.q_template_output_method_tab.get_rows()

        template = TemplateModel(
            id=template_id,
            test_resonator_id_1=test_resonator_ids[0],
            test_resonator_id_2=test_resonator_ids[1],
            test_resonator_id_3=test_resonator_ids[2],
            monster_id=monster_id,
            description=description,
            resonators=resonators,
            rows=rows,
        )

        return template

    def export_images(self):
        template = self.get_template()
        get_template_html_resonator_model(template.test_resonator_id_1)

    def save(self):
        self.q_progress_bar.set(0.0, _(ZhTwEnum.SAVING))

        template = self.get_template()
        if template.id == "":
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.TEMPLATE_ID_MUST_NOT_EMPTY)
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
        self.q_template_output_method_tab.load(template.rows)

        self.q_progress_bar.set(100.0, _(ZhTwEnum.LOADED))

    def delete(self):
        template_id = self.q_template_basic_tab.get_template_id()
        if not template_id:
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                _(ZhTwEnum.TO_SELECT_TEMPLATE_ID_TO_DELETE),
            )
            return

        self.q_progress_bar.reset()

        confirmation = QMessageBox.question(
            self,
            _(ZhTwEnum.DELETE),
            f"{_(ZhTwEnum.CONFIRM_DELETE_TEMPLATE)} '{template_id}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.No:
            return

        template_path = get_template_path(template_id)
        if not template_path.is_dir() and template_path.exists():
            template_path.unlink()
            self.q_template_basic_tab.reset_template_id()
