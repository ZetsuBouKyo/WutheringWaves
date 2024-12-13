from decimal import InvalidOperation

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import Damage
from ww.crud.resonator_damage_compare import (
    delete_resonator_damage_compare,
    get_resonator_damage_compare,
    get_resonator_damage_compare_fpath,
    get_resonator_damage_compare_ids,
    save_resonator_damage_compare,
)
from ww.html.image import (
    export_html_template_output_methods_as_png_by_template_id,
    export_resonator_damage_compare_as_png,
)
from ww.html.image.resonator_damage_compare import (
    get_export_resonator_damage_compare_home_path,
)
from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.model.damage_compare import DamageCompareModel
from ww.ui.calc.resonator_compare.table import (
    QResonatorDamageCompareTable,
    QResonatorDamageCompareUneditableTable,
    QResonatorDamageCompareUneditableTableEnum,
)
from ww.ui.combobox import QAutoCompleteComboBox


class QResonatorDamageCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Button 1
        self.q_btns_layout_1 = QHBoxLayout()
        self.q_id_label = QLabel(_(ZhTwEnum.ID))
        self.q_id_combobox = QAutoCompleteComboBox(
            getOptions=get_resonator_damage_compare_ids
        )
        self.q_id_combobox.setFixedHeight(40)
        self.q_id_combobox.setFixedWidth(600)
        self.q_new_btn = QPushButton(_(ZhTwEnum.NEW))
        self.q_new_btn.clicked.connect(self.new)
        self.q_save_btn = QPushButton(_(ZhTwEnum.SAVE))
        self.q_save_btn.clicked.connect(self.save)
        self.q_load_btn = QPushButton(_(ZhTwEnum.LOAD))
        self.q_load_btn.clicked.connect(self.load)
        self.q_delete_btn = QPushButton(_(ZhTwEnum.DELETE))
        self.q_delete_btn.clicked.connect(self.delete)
        self.q_btns_layout_1.addWidget(self.q_id_label)
        self.q_btns_layout_1.addWidget(self.q_id_combobox)
        self.q_btns_layout_1.addStretch()
        self.q_btns_layout_1.addWidget(self.q_new_btn)
        self.q_btns_layout_1.addWidget(self.q_save_btn)
        self.q_btns_layout_1.addWidget(self.q_load_btn)
        self.q_btns_layout_1.addWidget(self.q_delete_btn)

        # Button 2
        self.q_btns_layout_2 = QHBoxLayout()
        self.q_calculate_btn = QPushButton(_(ZhTwEnum.CALCULATE))
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_export_image_btn = QPushButton(_(ZhTwEnum.EXPORT_IMAGES))
        self.q_export_image_btn.clicked.connect(self.export_images)
        self.q_btns_layout_2.addStretch()
        self.q_btns_layout_2.addWidget(self.q_calculate_btn)
        self.q_btns_layout_2.addWidget(self.q_export_image_btn)

        # Tables
        self.q_damage_compare_table = QResonatorDamageCompareTable()
        self.q_calculated_label = QLabel(_(ZhTwEnum.CALCULATED_RESULTS))
        self.q_damage_compare_uneditable_table = (
            QResonatorDamageCompareUneditableTable()
        )

        self.layout.addLayout(self.q_btns_layout_1)
        self.layout.addLayout(self.q_btns_layout_2)
        self.layout.addWidget(self.q_damage_compare_table)
        self.layout.addWidget(self.q_calculated_label)
        self.layout.addWidget(self.q_damage_compare_uneditable_table)
        self.setLayout(self.layout)

    def new(self):
        self.q_id_combobox.setCurrentText("")
        self.q_damage_compare_table.reset_data()
        self.q_damage_compare_uneditable_table.reset_data()

    def save(self):
        id = self.q_id_combobox.currentText()
        if id == "":
            QMessageBox.warning(
                self, _(ZhTwEnum.WARNING), _(ZhTwEnum.ID_MUST_NOT_EMPTY)
            )
            return

        fpath = get_resonator_damage_compare_fpath(id)
        if fpath.exists():
            confirmation = QMessageBox.question(
                self,
                _(ZhTwEnum.FILE_EXISTS),
                f"{_(ZhTwEnum.FILE_OVERWRITE_OR_NOT)}'{id}'?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirmation == QMessageBox.No:
                return

        data = self.q_damage_compare_table.get_dict_data()
        data_model = DamageCompareModel(id=id, data=data)

        save_resonator_damage_compare(data_model)

    def load(self):
        id = self.q_id_combobox.currentText()
        if not id:
            return

        data_model = get_resonator_damage_compare(id)
        if data_model is None:
            return

        self.q_damage_compare_table.load_df_dict(data_model.data)

    def delete(self):
        id = self.q_id_combobox.currentText()

        if not id:
            QMessageBox.warning(
                self,
                _(ZhTwEnum.WARNING),
                _(ZhTwEnum.TO_SELECT_ID_TO_DELETE),
            )
            return

        confirmation = QMessageBox.question(
            self,
            _(ZhTwEnum.DELETE),
            f"{_(ZhTwEnum.CONFIRM_DELETE_FILE)} '{id}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.No:
            return

        if delete_resonator_damage_compare(id):
            self.new()

    def calculate(self):
        data = []
        damage_compare_table_data = self.q_damage_compare_table.get_current_data()
        for resonator_id_1, monster_id, template_id, label in damage_compare_table_data:
            damage = Damage(monster_id=monster_id)
            damage_distributions = damage.get_damage_distributions_with_labels(
                template_id,
                resonator_id_1,
                "",
                "",
                monster_id=monster_id,
                labels=[label],
            )
            if not damage_distributions:
                continue

            damage_distribution = damage_distributions[label]
            for (
                resonator_damage_distribution
            ) in damage_distribution.resonators.values():
                try:
                    resonator_id = resonator_damage_distribution.resonator_id
                    damage = f"{resonator_damage_distribution.damage:,.2f}"
                    damage_no_crit = (
                        f"{resonator_damage_distribution.damage_no_crit:,.2f}"
                    )
                    damage_crit = f"{resonator_damage_distribution.damage_crit:,.2f}"

                    basic = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.BASIC.name.lower()
                        )
                    )
                    heavy = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.HEAVY.name.lower()
                        )
                    )
                    skill = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.SKILL.name.lower()
                        )
                    )
                    liberation = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.LIBERATION.name.lower()
                        )
                    )
                    intro = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.INTRO.name.lower()
                        )
                    )
                    outro = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.OUTRO.name.lower()
                        )
                    )
                    echo = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.ECHO.name.lower()
                        )
                    )
                    none = (
                        resonator_damage_distribution.get_damage_string_with_percentage(
                            SkillBonusTypeEnum.NONE.name.lower()
                        )
                    )

                    calculated_row = {
                        QResonatorDamageCompareUneditableTableEnum.RESONATOR_ID.value: resonator_id,
                        QResonatorDamageCompareUneditableTableEnum.TEMPLATE_ID.value: template_id,
                        QResonatorDamageCompareUneditableTableEnum.LABEL.value: label,
                        QResonatorDamageCompareUneditableTableEnum.MONSTER_ID.value: monster_id,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE.value: damage,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_NO_CRIT.value: damage_no_crit,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_CRIT.value: damage_crit,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_BASIC.value: basic,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_HEAVY.value: heavy,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_SKILL.value: skill,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_LIBERATION.value: liberation,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_INTRO.value: intro,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_OUTRO.value: outro,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_ECHO.value: echo,
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_NONE.value: none,
                    }

                    # print(calculated_row)
                except InvalidOperation:
                    calculated_row = {
                        QResonatorDamageCompareUneditableTableEnum.RESONATOR_ID.value: "",
                        QResonatorDamageCompareUneditableTableEnum.TEMPLATE_ID.value: "",
                        QResonatorDamageCompareUneditableTableEnum.LABEL.value: "",
                        QResonatorDamageCompareUneditableTableEnum.MONSTER_ID.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_NO_CRIT.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_CRIT.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_BASIC.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_HEAVY.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_SKILL.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_LIBERATION.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_INTRO.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_OUTRO.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_ECHO.value: "",
                        QResonatorDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_NONE.value: "",
                    }
                data.append(calculated_row)
        if len(data) > 0:
            self.q_damage_compare_uneditable_table.load_dict(data)

    def export_images(self):
        id = self.q_id_combobox.currentText()
        if not id:
            return

        damage_compare_table_data = self.q_damage_compare_table.get_current_data()
        results = []
        templates = set()
        for resonator_id_1, monster_id, template_id, label in damage_compare_table_data:
            labels = [label]

            damage = Damage(monster_id=monster_id)
            damage_distributions = damage.get_damage_distributions_with_labels(
                template_id,
                resonator_id_1,
                "",
                "",
                monster_id=monster_id,
                labels=labels,
            )
            for label_name, damage_distribution in damage_distributions.items():
                results.append((label_name, damage_distribution))

            templates.add((template_id, label))

        export_resonator_damage_compare_as_png(id, results)

        export_home_path = get_export_resonator_damage_compare_home_path(id)
        for template_id, label in templates:
            export_html_template_output_methods_as_png_by_template_id(
                template_id, export_home_path, labels=[label]
            )
