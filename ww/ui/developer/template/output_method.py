from decimal import Decimal
from functools import partial
from typing import Dict, List, Optional

import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import Damage
from ww.crud.buff import (
    add_echo_buff_descriptions,
    add_echo_sonata_buff_descriptions,
    add_resonator_buff_descriptions,
    add_weapon_buff_descriptions,
    get_echo_buffs,
    get_echo_sonata_buffs,
    get_resonator_buffs,
    get_weapon_buffs,
)
from ww.crud.resonator import get_resonator_and_echo_skill_ids
from ww.locale import ZhTwEnum, _
from ww.model.template import (
    TEMPLATE_BONUS,
    CalculatedTemplateRowModel,
    TemplateBuffTableColumnEnum,
    TemplateBuffTableRowModel,
    TemplateColumnEnum,
    TemplateRowBuffTypeEnum,
    TemplateRowModel,
)
from ww.tables.echo import EchoSkillTable
from ww.tables.monster import MonstersTable, MonsterTsvColumnEnum
from ww.tables.resonator import CalculatedResonatorsTable, ResonatorsTable
from ww.ui.button import QDataPushButton
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.progress_bar import QHProgressBar
from ww.ui.table import QDraggableTableWidget
from ww.ui.table.cell import set_item, set_uneditable_cell
from ww.ui.table.cell.combobox import (
    set_action_combobox,
    set_buff_type_combobox,
    set_combobox,
    set_resonator_name_combobox,
    set_skill_bonus_type_combobox,
)
from ww.utils.number import get_number


class QTemplateTabOutputMethodBuffTable(QDraggableTableWidget):
    def __init__(
        self,
        rows: int,
        columns: int,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
        buffs: Dict[str, Dict[str, str]] = {},
    ):
        self.buffs = buffs
        self.buffs_list = [key for key in self.buffs.keys()]
        self.buffs_list.sort()

        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=column_id_name,
            column_names=column_names,
        )

        self.setColumnWidth(
            self.get_column_id(TemplateBuffTableColumnEnum.NAME.value), 500
        )

    def update_row(self, buff_primary_key: str):
        try:
            i = self.buffs_list.index(buff_primary_key)
        except ValueError:
            return
        row = self.get_selected_rows()[0]
        buff_id = self.buffs_list[i]
        buff = self.buffs.get(buff_id, {})
        buff_type = buff.get(_(ZhTwEnum.BUFF_TYPE), None)
        buff_value = buff.get(_(ZhTwEnum.BUFF_VALUE), None)
        buff_duration = buff.get(_(ZhTwEnum.BUFF_DURATION), None)
        buff_description = buff.get(_(ZhTwEnum.BUFF_DESCRIPTION), "")
        if not buff or buff_type is None or buff_value is None or buff_duration is None:
            return

        buff_name_col = self.get_column_id(TemplateBuffTableColumnEnum.NAME.value)
        buff_type_col = self.get_column_id(TemplateBuffTableColumnEnum.TYPE.value)
        buff_value_col = self.get_column_id(TemplateBuffTableColumnEnum.VALUE.value)
        buff_duration_col = self.get_column_id(
            TemplateBuffTableColumnEnum.DURATION.value
        )
        self.set_cell(row, buff_type_col, buff_type)
        self.set_cell(row, buff_value_col, buff_value)
        self.set_cell(row, buff_duration_col, buff_duration)

        cell = self.cellWidget(row, buff_name_col)
        cell.setToolTip(buff_description)

    def set_cell(self, row: int, col: int, value: str):
        try:
            if self.column_names[col] == TemplateBuffTableColumnEnum.NAME.value:
                buff = self.buffs.get(value, {})
                buff_description = buff.get(_(ZhTwEnum.BUFF_DESCRIPTION), "")

                combobox = set_combobox(
                    self, row, col, value, self.buffs_list, toolTip=buff_description
                )
                combobox.currentTextChanged.connect(self.update_row)
            elif self.column_names[col] == TemplateBuffTableColumnEnum.TYPE.value:
                set_buff_type_combobox(self, row, col, value)
            else:
                set_item(self, row, col, value)
        except IndexError:
            ...


class QTemplateTabOutputMethodTable(QDraggableTableWidget):
    def __init__(self, basic: QTemplateBasicTab, progress_bar: QHProgressBar):
        self.basic = basic
        self.progress_bar = progress_bar

        ouput_methods = [TemplateRowModel()]

        column_names = [e.value for e in TemplateColumnEnum]

        rows = len(ouput_methods)
        columns = len(column_names)

        self.ouput_methods = ouput_methods
        self.calculated_rows = []

        super().__init__(rows, columns, [], column_names=column_names)
        self.setHorizontalHeaderLabels(self.column_names)

    def insertRow(self, row: int):
        new_ouput_methods = (
            self.ouput_methods[:row] + [TemplateRowModel()] + self.ouput_methods[row:]
        )
        self.ouput_methods = new_ouput_methods
        super().insertRow(row)

    def removeRow(self, row: int):
        del self.ouput_methods[row]
        super().removeRow(row)

    def calculate(self, is_progress: bool = True):
        if is_progress:
            percentage = 0.0
            diff = 100.0 / self.rowCount() + 1
            self.progress_bar.set(percentage, _(ZhTwEnum.CALCULATING))

        self.calculated_rows = []
        for row in range(self.rowCount()):
            self.update_row_buffs(row, self.ouput_methods[row].buffs)
            calculated_row = self.calculate_row(row)
            if calculated_row is not None:
                self.calculated_rows.append(calculated_row)

            if is_progress:
                percentage += diff
                self.progress_bar.set_percentage(percentage)
        if is_progress:
            self.progress_bar.set(100.0, _(ZhTwEnum.CALCULATED))

    def remove_buffs(self, dialog: QDialog, line: QLineEdit):
        buff_name = line.text()
        if not buff_name:
            dialog.done(1)
        for i in range(len(self.ouput_methods)):
            buffs = self.ouput_methods[i].buffs
            new_buffs = []
            for buff in buffs:
                if buff.name == buff_name:
                    continue
                new_buffs.append(buff)
            self.ouput_methods[i].buffs = new_buffs
        self.calculate(is_progress=False)
        dialog.done(1)

    def delete_buffs(self):
        width = 1200
        height = 600
        center = QDesktopWidget().availableGeometry().center()
        x0 = center.x() - width // 2
        y0 = center.y() - height // 2

        layout = QVBoxLayout()

        dialog = QDialog(self)
        dialog.setWindowTitle("Wuthering Waves")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(x0, y0, width, height)

        line_layout = QHBoxLayout()
        label = QLabel(_(ZhTwEnum.BUFF_NAME_TO_DELETE))
        label.setFixedWidth(150)
        label.setFixedHeight(40)
        line = QLineEdit()
        line.setFixedWidth(200)
        line.setFixedHeight(40)
        line_layout.addWidget(label)
        line_layout.addWidget(line)
        line_layout.addStretch()

        btns_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(partial(self.remove_buffs, dialog, line))
        ok_btn.setFixedHeight(40)
        btns_layout.addStretch()
        btns_layout.addWidget(ok_btn)

        layout.addLayout(line_layout)
        layout.addStretch()
        layout.addLayout(btns_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def load(self, rows: List[TemplateRowModel]):
        self.ouput_methods = rows
        row = len(self.ouput_methods)
        self.setRowCount(row)
        self._init_cells()

    def _init_column_width(self):
        for e in TemplateColumnEnum:
            width = len(e.value) * 20 + 50
            col = self.get_column_id(e.value)
            self.setColumnWidth(col, width)
        skill_ids_col = self.get_column_id(TemplateColumnEnum.SKILL_ID.value)
        self.setColumnWidth(skill_ids_col, 400)

        result_skill_base_attr_col = self.get_column_id(
            TemplateColumnEnum.RESULT_SKILL_BASE_ATTRIBUTE.value
        )
        self.setColumnWidth(result_skill_base_attr_col, 200)

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.set_cell(row, col, None)
        self.calculate(is_progress=False)

    def _get_resonator_skill_ids(self) -> List[str]:
        row = self.get_selected_row()
        if row is None:
            return
        resonator_name = self._get_resonator_name(row)
        return get_resonator_and_echo_skill_ids(resonator_name)

    def _get_resonator_name(self, row: int) -> str:
        col = self.get_column_id(TemplateColumnEnum.RESONATOR_NAME.value)
        return self.get_cell(row, col)

    def update_row(self, row: int):
        # Resonator name
        col_resonator_name = self.get_column_id(TemplateColumnEnum.RESONATOR_NAME.value)
        self.ouput_methods[row].resonator_name = self.get_cell(row, col_resonator_name)

        # DMG no CRIT
        col_real_dmg_no_crit = self.get_column_id(
            TemplateColumnEnum.REAL_DMG_NO_CRIT.value
        )
        self.ouput_methods[row].real_dmg_no_crit = self.get_cell(
            row, col_real_dmg_no_crit
        )

        # DMG CRIT
        col_real_dmg_crit = self.get_column_id(TemplateColumnEnum.REAL_DMG_CRIT.value)
        self.ouput_methods[row].real_dmg_crit = self.get_cell(row, col_real_dmg_crit)

        # Action
        col_action = self.get_column_id(TemplateColumnEnum.ACTION.value)
        self.ouput_methods[row].action = self.get_cell(row, col_action)

        # Skill ID
        col_skill_id = self.get_column_id(TemplateColumnEnum.SKILL_ID.value)
        self.ouput_methods[row].skill_id = self.get_cell(row, col_skill_id)

        # Skill bonus type
        col_skill_bonus_type = self.get_column_id(
            TemplateColumnEnum.SKILL_BONUS_TYPE.value
        )
        self.ouput_methods[row].skill_bonus_type = self.get_cell(
            row, col_skill_bonus_type
        )

        # Concerto regen
        col_resonating_spin_concerto_regen = self.get_column_id(
            TemplateColumnEnum.RESONATING_SPIN_CONCERTO_REGEN.value
        )
        self.ouput_methods[row].resonating_spin_concerto_regen = self.get_cell(
            row, col_resonating_spin_concerto_regen
        )

        col_accumulated_resonating_spin_concerto_regen = self.get_column_id(
            TemplateColumnEnum.ACCUMULATED_RESONATING_SPIN_CONCERTO_REGEN.value
        )
        self.ouput_methods[row].accumulated_resonating_spin_concerto_regen = (
            self.get_cell(row, col_accumulated_resonating_spin_concerto_regen)
        )

        # Time
        col_time_start = self.get_column_id(TemplateColumnEnum.TIME_START.value)
        self.ouput_methods[row].time_start = self.get_cell(row, col_time_start)

        col_time_end = self.get_column_id(TemplateColumnEnum.TIME_END.value)
        self.ouput_methods[row].time_end = self.get_cell(row, col_time_end)

        col_cumulative_time = self.get_column_id(
            TemplateColumnEnum.CUMULATIVE_TIME.value
        )
        self.ouput_methods[row].cumulative_time = self.get_cell(
            row, col_cumulative_time
        )

        # Frame
        col_frame = self.get_column_id(TemplateColumnEnum.FRAME.value)
        self.ouput_methods[row].frame = self.get_cell(row, col_frame)

        # Buffs
        self.update_row_buffs(row, self.ouput_methods[row].buffs)

        return self.ouput_methods[row]

    def get_row(self, row: int) -> TemplateRowModel:
        self.update_row(row)
        return self.ouput_methods[row]

    def get_output_methods(self) -> List[TemplateRowModel]:
        for row in range(self.rowCount()):
            self.update_row(row)

        return self.ouput_methods

    def set_row(self, row: int, data: TemplateRowModel):
        if isinstance(data, TemplateRowModel):
            self.ouput_methods[row] = data
            for col in range(self.columnCount()):
                self.set_cell(row, col, None)

    def get_cell(self, row: int, col: int) -> str:
        cell = super().get_cell(row, col)
        if cell is None:
            cell = ""
        return cell

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == TemplateColumnEnum.COMMENT.value:
            btn = QDataPushButton(_(ZhTwEnum.COMMENT))
            btn.setToolTip(self.ouput_methods[row].comment)
            btn.clicked.connect(partial(self.add_comment, btn))
            self.setCellWidget(row, col, btn)
        elif self.column_names[col] == TemplateColumnEnum.CALCULATE.value:
            btn = QPushButton(_(ZhTwEnum.CALCULATE))
            btn.clicked.connect(partial(self.calculate_row, None))
            self.setCellWidget(row, col, btn)
        elif self.column_names[col] == TemplateColumnEnum.BONUS_BUFF.value:
            btn = QDataPushButton("+")
            btn.clicked.connect(partial(self.add_buff, btn))
            self.setCellWidget(row, col, btn)
        elif self.column_names[col] == TemplateColumnEnum.RESONATOR_NAME.value:
            set_resonator_name_combobox(
                self, row, col, self.ouput_methods[row].resonator_name
            )
        elif self.column_names[col] == TemplateColumnEnum.REAL_DMG_NO_CRIT.value:
            set_item(self, row, col, self.ouput_methods[row].real_dmg_no_crit)
        elif self.column_names[col] == TemplateColumnEnum.REAL_DMG_CRIT.value:
            set_item(self, row, col, self.ouput_methods[row].real_dmg_crit)
        elif self.column_names[col] == TemplateColumnEnum.ACTION.value:
            set_action_combobox(self, row, col, self.ouput_methods[row].action)
        elif self.column_names[col] == TemplateColumnEnum.SKILL_ID.value:
            set_combobox(
                self,
                row,
                col,
                self.ouput_methods[row].skill_id,
                [],
                getOptions=self._get_resonator_skill_ids,
            )
        elif self.column_names[col] == TemplateColumnEnum.SKILL_BONUS_TYPE.value:
            set_skill_bonus_type_combobox(
                self, row, col, self.ouput_methods[row].skill_bonus_type
            )
        elif (
            self.column_names[col] == TemplateColumnEnum.DAMAGE.value
            or self.column_names[col] == TemplateColumnEnum.DAMAGE_NO_CRIT.value
            or self.column_names[col] == TemplateColumnEnum.DAMAGE_CRIT.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_ELEMENT.value
            or self.column_names[col]
            == TemplateColumnEnum.RESULT_SKILL_BASE_ATTRIBUTE.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_BONUS_TYPE.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_SKILL_DMG.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_ATK.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_ATK_ADDITION.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_ATK_P.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_CRIT_RATE.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_CRIT_DMG.value
            or self.column_names[col] == TemplateColumnEnum.RESULT_BONUS.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_MAGNIFIER.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_AMPLIFIER.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_HP_P.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_HP.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_ATK_P.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_ATK.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_DEF_P.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_DEF.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_CRIT_RATE.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_CRIT_DMG.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_ADDITION.value
            or self.column_names[col]
            == TemplateColumnEnum.BONUS_SKILL_DMG_ADDITION.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_IGNORE_DEF.value
            or self.column_names[col] == TemplateColumnEnum.BONUS_REDUCE_RES.value
        ):
            set_uneditable_cell(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateColumnEnum.RESONATING_SPIN_CONCERTO_REGEN.value
        ):
            set_item(
                self, row, col, self.ouput_methods[row].resonating_spin_concerto_regen
            )
        elif (
            self.column_names[col]
            == TemplateColumnEnum.ACCUMULATED_RESONATING_SPIN_CONCERTO_REGEN.value
        ):
            set_item(
                self,
                row,
                col,
                self.ouput_methods[row].accumulated_resonating_spin_concerto_regen,
            )
        elif self.column_names[col] == TemplateColumnEnum.TIME_START.value:
            set_item(self, row, col, self.ouput_methods[row].time_start)
        elif self.column_names[col] == TemplateColumnEnum.TIME_END.value:
            set_item(self, row, col, self.ouput_methods[row].time_end)
        elif self.column_names[col] == TemplateColumnEnum.CUMULATIVE_TIME.value:
            set_item(self, row, col, self.ouput_methods[row].cumulative_time)
        elif self.column_names[col] == TemplateColumnEnum.FRAME.value:
            set_item(self, row, col, self.ouput_methods[row].frame)
        else:
            set_item(self, row, col, "")

    def get_row_buff(self, row: int) -> List[List[str]]:
        data = []
        output_method = self.ouput_methods[row]

        for buff in output_method.buffs:
            data.append([buff.name, buff.type, buff.value, buff.stack, buff.duration])
        if len(data) == 0:
            return [["", "", "", "", ""]]
        return data

    def update_row_buffs(self, row: int, buffs: List[TemplateBuffTableRowModel]):
        # TODO: refactor?
        buff_dict = {e.value: Decimal("0.0") for e in TemplateRowBuffTypeEnum}
        buff_data = {e.value: [] for e in TemplateBuffTableColumnEnum}

        for buff in buffs:
            # Tool tips
            buff_data[TemplateBuffTableColumnEnum.NAME.value].append(buff.name)
            buff_data[TemplateBuffTableColumnEnum.TYPE.value].append(buff.type)
            buff_data[TemplateBuffTableColumnEnum.VALUE.value].append(buff.value)
            buff_data[TemplateBuffTableColumnEnum.STACK.value].append(buff.stack)
            buff_data[TemplateBuffTableColumnEnum.DURATION.value].append(buff.duration)

            # Calculate
            value = get_number(buff.value) * get_number(buff.stack)
            t = buff_dict.get(buff.type, None)
            if t is None:
                continue
            buff_dict[buff.type] += value
        for buff_type, buff in buff_dict.items():
            buff_column_name = f"{TEMPLATE_BONUS}{buff_type}"
            col = self.get_column_id(buff_column_name)

            value = str(buff)
            if buff == get_number("0.0"):
                value = ""

            set_uneditable_cell(self, row, col, value)

        df = pd.DataFrame(buff_data)
        col = self.get_column_id(TemplateColumnEnum.BONUS_BUFF.value)
        buff_btn_cell = self.cellWidget(row, col)
        buff_btn_cell.setToolTip(df.to_html())

    def set_row_buff(
        self,
        row: int,
        dialog: QDialog,
        table: QDraggableTableWidget,
        btn: QDataPushButton,
    ):
        data = table.get_data()
        buffs = []
        for d in data:
            buff = TemplateBuffTableRowModel(
                name=d[0], type=d[1], value=d[2], stack=d[3], duration=d[4]
            )
            buffs.append(buff)
        btn.set_data(buffs)
        self.ouput_methods[row].buffs = buffs

        # Update following cells
        self.update_row_buffs(row, buffs)

        dialog.done(1)

    def set_row_comment(
        self, row: int, dialog: QDialog, text_edit: QTextEdit, btn: QDataPushButton
    ):
        text = text_edit.toPlainText()
        self.ouput_methods[row].comment = text
        btn.setToolTip(text)
        dialog.done(1)

    def add_default_buffs(
        self, to_buffs: Dict[str, Dict[str, str]], from_buffs: List[Dict[str, str]]
    ):
        for buff in from_buffs:
            buff_id = buff.get(_(ZhTwEnum.BUFF_ID), None)
            if buff_id is None:
                continue
            to_buffs[buff_id] = buff

    def get_default_buffs(self) -> Dict[str, Dict[str, str]]:
        buffs = {}
        sonatas = set()
        for resonator in self.basic.get_resonators():
            # Resonator
            resonator_name = resonator.resonator_name
            resonator_buffs = get_resonator_buffs(resonator_name)
            add_resonator_buff_descriptions(resonator_buffs)
            self.add_default_buffs(buffs, resonator_buffs)

            # Weapon
            weapon_name = resonator.resonator_weapon_name
            weapon_buffs = get_weapon_buffs(weapon_name)
            add_weapon_buff_descriptions(weapon_buffs)
            self.add_default_buffs(buffs, weapon_buffs)

            # Echo
            echo_name = resonator.resonator_echo_1
            echo_buffs = get_echo_buffs(echo_name)
            add_echo_buff_descriptions(echo_buffs)
            self.add_default_buffs(buffs, echo_buffs)

            # Echo sonata
            resonator_sonatas = [
                resonator.resonator_echo_sonata_1,
                resonator.resonator_echo_sonata_2,
                resonator.resonator_echo_sonata_3,
                resonator.resonator_echo_sonata_4,
                resonator.resonator_echo_sonata_5,
            ]
            sonata_count = {}
            for sonata in resonator_sonatas:
                if sonata_count.get(sonata, None) is None:
                    sonata_count[sonata] = 1
                else:
                    sonata_count[sonata] += 1
            for sonata, count in sonata_count.items():
                if count >= 5:
                    sonatas.add(sonata)

        echo_sonata_buffs = []
        for sonata in sonatas:
            echo_sonata_buffs += get_echo_sonata_buffs(sonata)
        add_echo_sonata_buff_descriptions(echo_sonata_buffs)
        self.add_default_buffs(buffs, echo_sonata_buffs)

        return buffs

    def calculate_row(self, row: Optional[int]) -> Optional[CalculatedTemplateRowModel]:
        if row is None:
            row = self.get_selected_row()
            if row is None:
                return
        row_data = self.get_row(row)

        name_to_id = self.basic.get_test_resonators()
        monster_id = self.basic.get_monster_id()

        resonator_name = row_data.resonator_name
        resonator_id = name_to_id.get(resonator_name, None)
        if resonator_id is None:
            return

        damage = Damage(monster_id=monster_id)
        calculated_row = damage.get_calculated_row(resonator_id, row_data)

        if calculated_row is None:
            return

        col_dmg_names = [
            TemplateColumnEnum.DAMAGE_NO_CRIT,
            TemplateColumnEnum.DAMAGE_CRIT,
            TemplateColumnEnum.DAMAGE,
        ]
        for col_name in col_dmg_names:
            col_index = self.get_column_id(col_name.value)
            value = getattr(calculated_row, col_name.name.lower(), "")
            if value == get_number("0.0"):
                value = ""
            elif type(value) == Decimal:
                value = f"{value:,.2f}"

            self.set_cell(row, col_index, value)

        col_names = [
            TemplateColumnEnum.RESULT_BONUS_TYPE,
            TemplateColumnEnum.RESULT_ELEMENT,
            TemplateColumnEnum.RESULT_SKILL_BASE_ATTRIBUTE,
            TemplateColumnEnum.RESULT_SKILL_DMG,
            TemplateColumnEnum.RESULT_ATK,
            TemplateColumnEnum.RESULT_ATK_ADDITION,
            TemplateColumnEnum.RESULT_ATK_P,
            TemplateColumnEnum.RESULT_CRIT_RATE,
            TemplateColumnEnum.RESULT_CRIT_DMG,
            TemplateColumnEnum.RESULT_BONUS,
        ]
        for col_name in col_names:
            col_index = self.get_column_id(col_name.value)
            value = getattr(calculated_row, col_name.name.lower(), "")
            if value == get_number("0.0"):
                value = ""
            else:
                value = str(value)

            self.set_cell(row, col_index, value)
        return calculated_row

    def add_comment(self, btn: QDataPushButton):
        row = self.get_selected_row()
        if row is None:
            return

        width = 1200
        height = 600
        center = QDesktopWidget().availableGeometry().center()
        x0 = center.x() - width // 2
        y0 = center.y() - height // 2

        layout = QVBoxLayout()

        dialog = QDialog(self)
        dialog.setWindowTitle("Wuthering Waves Template Buff")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(x0, y0, width, height)

        text = self.ouput_methods[row].comment
        text_edit = QTextEdit()
        text_edit.setText(text)

        btns_layout = QHBoxLayout()
        ok_btn = QDataPushButton("OK")
        ok_btn.clicked.connect(
            partial(self.set_row_comment, row, dialog, text_edit, btn)
        )
        ok_btn.setFixedHeight(40)
        btns_layout.addStretch()
        btns_layout.addWidget(ok_btn)

        layout.addWidget(text_edit)
        layout.addLayout(btns_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def add_buff(self, btn: QDataPushButton):
        row = self.get_selected_row()
        if row is None:
            return

        buffs = self.get_default_buffs()

        width = 1200
        height = 600
        center = QDesktopWidget().availableGeometry().center()
        x0 = center.x() - width // 2
        y0 = center.y() - height // 2

        layout = QVBoxLayout()

        dialog = QDialog(self)
        dialog.setWindowTitle("Wuthering Waves Template Buff")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(x0, y0, width, height)

        data = self.get_row_buff(row)

        column_names = [e.value for e in TemplateBuffTableColumnEnum]
        table = QTemplateTabOutputMethodBuffTable(
            len(data),
            len(column_names),
            data=data,
            column_names=column_names,
            buffs=buffs,
        )

        btns_layout = QHBoxLayout()
        ok_btn = QDataPushButton("OK")
        ok_btn.clicked.connect(partial(self.set_row_buff, row, dialog, table, btn))
        ok_btn.setFixedHeight(40)
        btns_layout.addStretch()
        btns_layout.addWidget(ok_btn)

        layout.addWidget(table)
        layout.addLayout(btns_layout)

        dialog.setLayout(layout)
        dialog.exec_()


class QTemplateOutputMethodTab(QWidget):

    def __init__(self, basic: QTemplateBasicTab, progress_bar: QHProgressBar):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_calculate_btn = QPushButton(_(ZhTwEnum.CALCULATE))
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_delete_buffs_btn = QPushButton(_(ZhTwEnum.DELETE_BUFFS))
        self.q_delete_buffs_btn.clicked.connect(self.delete_buffs)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_delete_buffs_btn)
        self.q_btns_layout.addWidget(self.q_calculate_btn)

        self.q_output_method_table = QTemplateTabOutputMethodTable(basic, progress_bar)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_output_method_table)

        self.setLayout(self.layout)

    def calculate(self):
        self.q_output_method_table.calculate()

    def delete_buffs(self):
        self.q_output_method_table.delete_buffs()

    def load(self, rows: List[TemplateRowModel]):
        self.q_output_method_table.load(rows)

    def get_rows(self) -> List[TemplateRowModel]:
        return self.q_output_method_table.get_output_methods()

    def get_rows(self) -> List[TemplateRowModel]:
        return self.q_output_method_table.get_output_methods()
