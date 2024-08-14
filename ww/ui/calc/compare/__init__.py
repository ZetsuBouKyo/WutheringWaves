from decimal import Decimal, InvalidOperation

from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ww.calc.damage import get_json_damage
from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.model.resonators import ResonatorsEnum
from ww.tables.resonators import ResonatorsTable
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

                damage_distribution = {
                    SkillBonusTypeEnum.BASIC.value: Decimal("0.0"),
                    SkillBonusTypeEnum.HEAVY.value: Decimal("0.0"),
                    SkillBonusTypeEnum.SKILL.value: Decimal("0.0"),
                    SkillBonusTypeEnum.LIBERATION.value: Decimal("0.0"),
                    SkillBonusTypeEnum.INTRO.value: Decimal("0.0"),
                    SkillBonusTypeEnum.OUTRO.value: Decimal("0.0"),
                    SkillBonusTypeEnum.ECHO.value: Decimal("0.0"),
                    SkillBonusTypeEnum.NONE.value: Decimal("0.0"),
                }

                resonator_name = resonators_table.search(
                    resonator_id, ResonatorsEnum.NAME
                )
                rows = get_json_damage(template_id, monster_id, resonator_id, "", "")
                for row in rows:
                    row_resonator_name = row.resonator_name
                    if row_resonator_name != resonator_name:
                        continue
                    row_damage = row.damage
                    row_damage_no_crit = row.damage_no_crit
                    row_damage_crit = row.damage_crit
                    row_bonus_type = row.result_bonus_type

                    damage_distribution[row_bonus_type] += row_damage

                    damage += row_damage
                    damage_no_crit += row_damage_no_crit
                    damage_crit += row_damage_crit
                    # print(row_damage, row_damage_no_crit, row_damage_crit)

                for key in damage_distribution.keys():
                    percentage = damage_distribution[key] / damage

                    percentage_str = f"{percentage:.2%}"

                    damage_distribution_str = f"{damage_distribution[key]:.2f}"

                    damage_distribution[key] = (
                        f"{damage_distribution_str} ({percentage_str})"
                    )

                damage = f"{damage:.2f}"
                damage_no_crit = f"{damage_no_crit:.2f}"
                damage_crit = f"{damage_crit:.2f}"

                calculated_row = {
                    QDamageCompareUneditableTableEnum.RESONATOR_ID.value: resonator_id,
                    QDamageCompareUneditableTableEnum.MONSTER_ID.value: monster_id,
                    QDamageCompareUneditableTableEnum.DAMAGE.value: damage,
                    QDamageCompareUneditableTableEnum.DAMAGE_NO_CRIT.value: damage_no_crit,
                    QDamageCompareUneditableTableEnum.DAMAGE_CRIT.value: damage_crit,
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_BASIC.value: damage_distribution[
                        SkillBonusTypeEnum.BASIC.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_HEAVY.value: damage_distribution[
                        SkillBonusTypeEnum.HEAVY.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_SKILL.value: damage_distribution[
                        SkillBonusTypeEnum.SKILL.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_LIBERATION.value: damage_distribution[
                        SkillBonusTypeEnum.LIBERATION.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_INTRO.value: damage_distribution[
                        SkillBonusTypeEnum.INTRO.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_OUTRO.value: damage_distribution[
                        SkillBonusTypeEnum.OUTRO.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_ECHO.value: damage_distribution[
                        SkillBonusTypeEnum.ECHO.value
                    ],
                    QDamageCompareUneditableTableEnum.DAMAGE_DISTRIBUTION_NONE.value: damage_distribution[
                        SkillBonusTypeEnum.NONE.value
                    ],
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
