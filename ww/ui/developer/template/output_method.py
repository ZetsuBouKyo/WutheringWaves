from decimal import Decimal
from functools import partial
from typing import Dict, List, Optional

import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import get_json_row_damage
from ww.crud.buff import (
    get_echo_buffs,
    get_echo_sonata_buffs,
    get_resonator_buffs,
    get_weapon_buffs,
)
from ww.crud.resonator import get_resonator_and_echo_skill_ids, get_resonator_names
from ww.locale import ZhHantEnum, _
from ww.model.buff import BUFF_DURATION, BUFF_ID, BUFF_TYPE, BUFF_VALUE
from ww.model.resonator_skill import ResonatorSkillBonusTypeEnum
from ww.model.template import (
    TEMPLATE_BONUS,
    CalculatedTemplateRowModel,
    TemplateBuffTableRowEnum,
    TemplateBuffTableRowModel,
    TemplateRowActionEnum,
    TemplateRowBuffTypeEnum,
    TemplateRowEnum,
    TemplateRowModel,
)
from ww.tables.echo import EchoSkillTable
from ww.tables.monster import MonstersEnum, MonstersTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.ui.button import QDataPushButton
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.progress_bar import QHProgressBar
from ww.ui.table import QDraggableTableWidget
from ww.ui.table.cell import set_uneditable_cell
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
            self.get_column_id(TemplateBuffTableRowEnum.NAME.value), 500
        )

    def update_row(self, i: int):
        row = self.get_selected_rows()[0]
        buff_id = self.buffs_list[i]
        buff = self.buffs.get(buff_id, {})
        buff_type = buff.get(BUFF_TYPE, None)
        buff_value = buff.get(BUFF_VALUE, None)
        buff_duration = buff.get(BUFF_DURATION, None)
        if not buff or buff_type is None or buff_value is None or buff_duration is None:
            return
        buff_type_col = self.get_column_id(TemplateBuffTableRowEnum.TYPE.value)
        buff_value_col = self.get_column_id(TemplateBuffTableRowEnum.VALUE.value)
        buff_duration_col = self.get_column_id(TemplateBuffTableRowEnum.DURATION.value)
        self.set_cell(buff_type, row, buff_type_col)
        self.set_cell(buff_value, row, buff_value_col)
        self.set_cell(buff_duration, row, buff_duration_col)

    def set_cell(self, value: str, row: int, col: int):
        try:
            if self.column_names[col] == TemplateBuffTableRowEnum.NAME.value:
                combobox = self.set_combobox(row, col, value, self.buffs_list)
                combobox.currentIndexChanged.connect(self.update_row)
            elif self.column_names[col] == TemplateBuffTableRowEnum.TYPE.value:
                self.set_combobox(
                    row, col, value, [e.value for e in TemplateRowBuffTypeEnum]
                )
            else:
                item = QTableWidgetItem(value)
                self.setItem(row, col, item)
        except IndexError:
            ...


class QTemplateTabOutputMethodTable(QDraggableTableWidget):
    def __init__(self, basic: QTemplateBasicTab, progress_bar: QHProgressBar):
        self.basic = basic
        self.progress_bar = progress_bar

        ouput_methods = [TemplateRowModel()]

        column_names = [e.value for e in TemplateRowEnum]

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
            self.progress_bar.set(percentage, _(ZhHantEnum.CALCULATING))

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
            self.progress_bar.set(100.0, _(ZhHantEnum.CALCULATED))

    def load(self, rows: List[TemplateRowModel]):
        self.ouput_methods = rows
        row = len(self.ouput_methods)
        self.setRowCount(row)
        self._init_cells()

    def _init_column_width(self):
        for e in TemplateRowEnum:
            width = len(e.value) * 20 + 50
            col = self.get_column_id(e.value)
            self.setColumnWidth(col, width)
        skill_ids_col = self.get_column_id(TemplateRowEnum.SKILL_ID.value)
        self.setColumnWidth(skill_ids_col, 400)

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.set_cell(None, row, col)
        self.calculate(is_progress=False)

    def _get_resonator_skill_ids(self, row: int) -> str:
        resonator_name = self._get_resonator_name(row)
        return get_resonator_and_echo_skill_ids(resonator_name)

    def _get_resonator_name(self, row: int) -> str:
        col = self.get_column_id(TemplateRowEnum.RESONATOR_NAME.value)
        return self.get_cell(row, col)

    def update_row(self, row: int):
        # Resonator name
        col_resonator_name = self.get_column_id(TemplateRowEnum.RESONATOR_NAME.value)
        self.ouput_methods[row].resonator_name = self.get_cell(row, col_resonator_name)

        # DMG no CRIT
        col_real_dmg_no_crit = self.get_column_id(
            TemplateRowEnum.REAL_DMG_NO_CRIT.value
        )
        self.ouput_methods[row].real_dmg_no_crit = self.get_cell(
            row, col_real_dmg_no_crit
        )

        # DMG CRIT
        col_real_dmg_crit = self.get_column_id(TemplateRowEnum.REAL_DMG_CRIT.value)
        self.ouput_methods[row].real_dmg_crit = self.get_cell(row, col_real_dmg_crit)

        # Action
        col_action = self.get_column_id(TemplateRowEnum.ACTION.value)
        self.ouput_methods[row].action = self.get_cell(row, col_action)

        # Skill ID
        col_skill_id = self.get_column_id(TemplateRowEnum.SKILL_ID.value)
        self.ouput_methods[row].skill_id = self.get_cell(row, col_skill_id)

        # Skill bonus type
        col_skill_bonus_type = self.get_column_id(
            TemplateRowEnum.SKILL_BONUS_TYPE.value
        )
        self.ouput_methods[row].skill_bonus_type = self.get_cell(
            row, col_skill_bonus_type
        )

        # Concerto regen
        col_resonating_spin_concerto_regen = self.get_column_id(
            TemplateRowEnum.RESONATING_SPIN_CONCERTO_REGEN.value
        )
        self.ouput_methods[row].resonating_spin_concerto_regen = self.get_cell(
            row, col_resonating_spin_concerto_regen
        )

        col_accumulated_resonating_spin_concerto_regen = self.get_column_id(
            TemplateRowEnum.ACCUMULATED_RESONATING_SPIN_CONCERTO_REGEN.value
        )
        self.ouput_methods[row].accumulated_resonating_spin_concerto_regen = (
            self.get_cell(row, col_accumulated_resonating_spin_concerto_regen)
        )

        # Time
        col_time_start = self.get_column_id(TemplateRowEnum.TIME_START.value)
        self.ouput_methods[row].time_start = self.get_cell(row, col_time_start)

        col_time_end = self.get_column_id(TemplateRowEnum.TIME_END.value)
        self.ouput_methods[row].time_end = self.get_cell(row, col_time_end)

        col_cumulative_time = self.get_column_id(TemplateRowEnum.CUMULATIVE_TIME.value)
        self.ouput_methods[row].cumulative_time = self.get_cell(
            row, col_cumulative_time
        )

        # Frame
        col_frame = self.get_column_id(TemplateRowEnum.FRAME.value)
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
                self.set_cell(None, row, col)

    def get_cell(self, row: int, col: int) -> str:
        cell = super().get_cell(row, col)
        if cell is None:
            cell = ""
        return cell

    def update_cell(self, row: int, col: int, options: List[str], option_index: int):
        # TODO:
        ...

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == TemplateRowEnum.CALCULATE.value:
            btn = QDataPushButton(_(ZhHantEnum.CALCULATE))
            btn.clicked.connect(partial(self.calculate_row, None))
            self.setCellWidget(row, col, btn)
        elif self.column_names[col] == TemplateRowEnum.BONUS_BUFF.value:
            btn = QDataPushButton("+")
            btn.clicked.connect(partial(self.add_buff, btn))
            self.setCellWidget(row, col, btn)
        elif self.column_names[col] == TemplateRowEnum.RESONATOR_NAME.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].resonator_name,
                [],
                currentIndexChanged=self.update_cell,
                getOptions=get_resonator_names,
            )
        elif self.column_names[col] == TemplateRowEnum.REAL_DMG_NO_CRIT.value:
            self.set_item(self.ouput_methods[row].real_dmg_no_crit, row, col)
        elif self.column_names[col] == TemplateRowEnum.REAL_DMG_CRIT.value:
            self.set_item(self.ouput_methods[row].real_dmg_crit, row, col)
        elif self.column_names[col] == TemplateRowEnum.ACTION.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].action,
                [e.value for e in TemplateRowActionEnum],
            )
        elif self.column_names[col] == TemplateRowEnum.SKILL_ID.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].skill_id,
                [],
                getOptions=partial(self._get_resonator_skill_ids, row),
            )
        elif self.column_names[col] == TemplateRowEnum.SKILL_BONUS_TYPE.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].skill_bonus_type,
                [e.value for e in ResonatorSkillBonusTypeEnum],
            )

        elif (
            self.column_names[col] == TemplateRowEnum.DAMAGE.value
            or self.column_names[col] == TemplateRowEnum.DAMAGE_NO_CRIT.value
            or self.column_names[col] == TemplateRowEnum.DAMAGE_CRIT.value
            or self.column_names[col] == TemplateRowEnum.FINAL_ELEMENT.value
            or self.column_names[col] == TemplateRowEnum.FINAL_BONUS_TYPE.value
            or self.column_names[col] == TemplateRowEnum.FINAL_SKILL_DMG.value
            or self.column_names[col] == TemplateRowEnum.FINAL_ATK.value
            or self.column_names[col] == TemplateRowEnum.FINAL_ATK_ADDITION.value
            or self.column_names[col] == TemplateRowEnum.FINAL_ATK_P.value
            or self.column_names[col] == TemplateRowEnum.FINAL_CRIT_RATE.value
            or self.column_names[col] == TemplateRowEnum.FINAL_CRIT_DMG.value
            or self.column_names[col] == TemplateRowEnum.FINAL_BONUS.value
            or self.column_names[col] == TemplateRowEnum.BONUS_MAGNIFIER.value
            or self.column_names[col] == TemplateRowEnum.BONUS_AMPLIFIER.value
            or self.column_names[col] == TemplateRowEnum.BONUS_HP_P.value
            or self.column_names[col] == TemplateRowEnum.BONUS_HP.value
            or self.column_names[col] == TemplateRowEnum.BONUS_ATK_P.value
            or self.column_names[col] == TemplateRowEnum.BONUS_ATK.value
            or self.column_names[col] == TemplateRowEnum.BONUS_DEF_P.value
            or self.column_names[col] == TemplateRowEnum.BONUS_DEF.value
            or self.column_names[col] == TemplateRowEnum.BONUS_CRIT_RATE.value
            or self.column_names[col] == TemplateRowEnum.BONUS_CRIT_DMG.value
            or self.column_names[col] == TemplateRowEnum.BONUS_ADDITION.value
            or self.column_names[col] == TemplateRowEnum.BONUS_SKILL_DMG_ADDITION.value
            or self.column_names[col] == TemplateRowEnum.BONUS_IGNORE_DEF.value
            or self.column_names[col] == TemplateRowEnum.BONUS_REDUCE_RES.value
        ):
            set_uneditable_cell(self, value, row, col)
        else:
            item = QTableWidgetItem("")
            self.setItem(row, col, item)

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
        buff_data = {e.value: [] for e in TemplateBuffTableRowEnum}

        for buff in buffs:
            # Tool tips
            buff_data[TemplateBuffTableRowEnum.NAME.value].append(buff.name)
            buff_data[TemplateBuffTableRowEnum.TYPE.value].append(buff.type)
            buff_data[TemplateBuffTableRowEnum.VALUE.value].append(buff.value)
            buff_data[TemplateBuffTableRowEnum.STACK.value].append(buff.stack)
            buff_data[TemplateBuffTableRowEnum.DURATION.value].append(buff.duration)

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

            set_uneditable_cell(self, value, row, col)

        df = pd.DataFrame(buff_data)
        col = self.get_column_id(TemplateRowEnum.BONUS_BUFF.value)
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

    def add_default_buffs(
        self, to_buffs: Dict[str, Dict[str, str]], from_buffs: List[Dict[str, str]]
    ):
        for buff in from_buffs:
            buff_id = buff.get(BUFF_ID, None)
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
            self.add_default_buffs(buffs, resonator_buffs)

            # Weapon
            weapon_name = resonator.resonator_weapon_name
            weapon_buffs = get_weapon_buffs(weapon_name)
            self.add_default_buffs(buffs, weapon_buffs)

            # Echo
            echo_name = resonator.resonator_echo_1
            echo_buffs = get_echo_buffs(echo_name)
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
        for sonata in sonatas:
            echo_sonata_buffs = get_echo_sonata_buffs(sonata)
            self.add_default_buffs(buffs, echo_sonata_buffs)

        return buffs

    def calculate_row(self, row: Optional[int]) -> Optional[CalculatedTemplateRowModel]:
        if row is None:
            selected_rows = self.get_selected_rows()
            if len(selected_rows) != 1:
                return
            row = selected_rows[0]
        data = self.get_row(row)

        name_to_id = self.basic.get_test_resonators()
        monster_id = self.basic.get_monster_id()

        resonator_name = data.resonator_name
        resonator_id = name_to_id.get(resonator_name, None)
        if resonator_id is None:
            return

        resonators_table = ResonatorsTable()
        calculated_resonators_table = CalculatedResonatorsTable()
        echo_skill_table = EchoSkillTable()
        monsters_table = MonstersTable()

        monster_level = get_number(
            monsters_table.search(monster_id, MonstersEnum.LEVEL)
        )
        monster_def = get_number(monsters_table.search(monster_id, MonstersEnum.DEF))

        calculated_row = get_json_row_damage(
            data,
            resonator_id,
            resonator_name,
            monster_id,
            monster_level,
            monster_def,
            resonators_table,
            calculated_resonators_table,
            echo_skill_table,
            monsters_table,
            _,
        )
        if calculated_row is None:
            return

        col_dmg_names = [
            TemplateRowEnum.DAMAGE_NO_CRIT,
            TemplateRowEnum.DAMAGE_CRIT,
            TemplateRowEnum.DAMAGE,
        ]
        for col_name in col_dmg_names:
            col_index = self.get_column_id(col_name.value)
            value = getattr(calculated_row, col_name.name.lower(), "")
            if value == get_number("0.0"):
                value = ""
            elif type(value) == Decimal:
                value = f"{value:.2f}"

            self.set_cell(value, row, col_index)

        col_names = [
            TemplateRowEnum.FINAL_ELEMENT,
            TemplateRowEnum.FINAL_BONUS_TYPE,
            TemplateRowEnum.FINAL_SKILL_DMG,
            TemplateRowEnum.FINAL_ATK,
            TemplateRowEnum.FINAL_ATK_ADDITION,
            TemplateRowEnum.FINAL_ATK_P,
            TemplateRowEnum.FINAL_CRIT_RATE,
            TemplateRowEnum.FINAL_CRIT_DMG,
            TemplateRowEnum.FINAL_BONUS,
        ]
        for col_name in col_names:
            col_index = self.get_column_id(col_name.value)
            value = getattr(calculated_row, col_name.name.lower(), "")
            if value == get_number("0.0"):
                value = ""
            else:
                value = str(value)

            self.set_cell(value, row, col_index)
        return calculated_row

    def add_buff(self, btn: QDataPushButton):
        selected_rows = self.get_selected_rows()
        if len(selected_rows) != 1:
            return
        row = selected_rows[0]

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

        column_names = [e.value for e in TemplateBuffTableRowEnum]
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
        self.q_calculate_btn = QPushButton(_(ZhHantEnum.CALCULATE))
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_calculate_btn)

        self.q_output_method_table = QTemplateTabOutputMethodTable(basic, progress_bar)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_output_method_table)

        self.setLayout(self.layout)

    def calculate(self):
        self.q_output_method_table.calculate()

    def load(self, rows: List[TemplateRowModel]):
        self.q_output_method_table.load(rows)

    def get_rows(self) -> List[TemplateRowModel]:
        return self.q_output_method_table.get_output_methods()
