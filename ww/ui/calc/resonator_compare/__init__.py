from decimal import InvalidOperation

from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ww.calc.damage import Damage
from ww.html.template import export_damage_distribution_as_png
from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.ui.calc.resonator_compare.table import (
    QResonatorDamageCompareTable,
    QResonatorDamageCompareUneditableTable,
    QResonatorDamageCompareUneditableTableEnum,
)


class QResonatorDamageCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_damage_compare_table = QResonatorDamageCompareTable()
        self.q_damage_compare_uneditable_table = (
            QResonatorDamageCompareUneditableTable()
        )

        self.q_calculated_label = QLabel("計算結果")

        self.q_btns_layout = QHBoxLayout()
        self.q_calculate_btn = QPushButton(_(ZhTwEnum.CALCULATE))
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_export_image_btn = QPushButton(_(ZhTwEnum.EXPORT_IMAGES))
        self.q_export_image_btn.clicked.connect(self.export_images)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_export_image_btn)
        self.q_btns_layout.addWidget(self.q_calculate_btn)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_damage_compare_table)
        self.layout.addWidget(self.q_calculated_label)
        self.layout.addWidget(self.q_damage_compare_uneditable_table)
        self.setLayout(self.layout)

    def calculate(self):
        data = []
        damage_compare_table_data = self.q_damage_compare_table.get_current_data()
        for (
            resonator_id_1,
            resonator_id_2,
            resonator_id_3,
            monster_id,
            template_id,
        ) in damage_compare_table_data:

            damage = Damage(monster_id=monster_id)
            damage_distribution = damage.get_damage_distribution(
                template_id,
                resonator_id_1,
                resonator_id_2,
                resonator_id_3,
                monster_id=monster_id,
            )

            for (
                resonator_damage_distribution
            ) in damage_distribution.resonators.values():
                try:
                    resonater_id = resonator_damage_distribution.resonater_id
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
                        QResonatorDamageCompareUneditableTableEnum.RESONATOR_ID.value: resonater_id,
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

        self.q_damage_compare_uneditable_table.load_dict(data)

    def export_images(self):
        damage_compare_table_data = self.q_damage_compare_table.get_current_data()
        damage_distributions = []
        for (
            resonator_id_1,
            resonator_id_2,
            resonator_id_3,
            monster_id,
            template_id,
        ) in damage_compare_table_data:

            damage = Damage(monster_id=monster_id)
            damage_distribution = damage.get_damage_distribution(
                template_id,
                resonator_id_1,
                resonator_id_2,
                resonator_id_3,
                monster_id=monster_id,
            )
            damage_distributions.append(damage_distribution)
        # export_damage_distribution_as_png("test", damage_distributions)