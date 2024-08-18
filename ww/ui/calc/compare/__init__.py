from decimal import Decimal, InvalidOperation

from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ww.calc.damage import Damage
from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.model.resonator import ResonatorTsvColumnEnum
from ww.tables.resonator import ResonatorsTable
from ww.ui.calc.compare.table import (
    QDamageCompareTable,
    QDamageCompareUneditableTable,
    QDamageCompareUneditableTableEnum,
)


class QDamageCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_damage_compare_table = QDamageCompareTable()
        self.q_damage_compare_uneditable_table = QDamageCompareUneditableTable()

        self.q_calculated_label = QLabel("計算結果")

        self.q_calculate_btn_layout = QHBoxLayout()
        self.q_calculate_btn = QPushButton(_(ZhTwEnum.CALCULATE))
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_calculate_btn_layout.addStretch()
        self.q_calculate_btn_layout.addWidget(self.q_calculate_btn)

        self.layout.addLayout(self.q_calculate_btn_layout)
        self.layout.addWidget(self.q_damage_compare_table)
        self.layout.addWidget(self.q_calculated_label)
        self.layout.addWidget(self.q_damage_compare_uneditable_table)
        self.setLayout(self.layout)

    def calculate(self):
        data = []
        resonators_table = ResonatorsTable()
        damage_compare_table_data = self.q_damage_compare_table.get_current_data()
        for resonator_id, monster_id, template_id in damage_compare_table_data:
            try:
                damage = Decimal("0.0")
                damage_no_crit = Decimal("0.0")
                damage_crit = Decimal("0.0")

                resonator_name = resonators_table.search(
                    resonator_id, ResonatorTsvColumnEnum.NAME
                )

                damage = Damage(monster_id=monster_id)
                damage_distributions = damage.get_damage_distribution(
                    template_id, resonator_id, "", "", monster_id=monster_id
                )

                damage_distribution = damage_distributions.resonators[resonator_name]

                damage = f"{damage_distribution.damage:.2f}"
                damage_no_crit = f"{damage_distribution.damage_no_crit:.2f}"
                damage_crit = f"{damage_distribution.damage_crit:.2f}"

                basic = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.BASIC.name.lower()
                )
                heavy = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.HEAVY.name.lower()
                )
                skill = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.SKILL.name.lower()
                )
                liberation = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.LIBERATION.name.lower()
                )
                intro = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.INTRO.name.lower()
                )
                outro = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.OUTRO.name.lower()
                )
                echo = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.ECHO.name.lower()
                )
                none = damage_distribution.get_damage_string_with_percentage(
                    SkillBonusTypeEnum.NONE.name.lower()
                )

                calculated_row = {
                    QDamageCompareUneditableTableEnum.RESONATOR_ID.value: resonator_id,
                    QDamageCompareUneditableTableEnum.MONSTER_ID.value: monster_id,
                    QDamageCompareUneditableTableEnum.DAMAGE.value: damage,
                    QDamageCompareUneditableTableEnum.DAMAGE_NO_CRIT.value: damage_no_crit,
                    QDamageCompareUneditableTableEnum.DAMAGE_CRIT.value: damage_crit,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_BASIC.value: basic,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_HEAVY.value: heavy,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_SKILL.value: skill,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_LIBERATION.value: liberation,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_INTRO.value: intro,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_OUTRO.value: outro,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_ECHO.value: echo,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_NONE.value: none,
                }
                # print(calculated_row)
            except InvalidOperation:
                calculated_row = {
                    QDamageCompareUneditableTableEnum.RESONATOR_ID.value: "",
                    QDamageCompareUneditableTableEnum.MONSTER_ID.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_NO_CRIT.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_CRIT.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_BASIC.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_HEAVY.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_SKILL.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_LIBERATION.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_INTRO.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_OUTRO.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_ECHO.value: "",
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_NONE.value: "",
                }
            data.append(calculated_row)
        self.q_damage_compare_uneditable_table.load_dict(data)
