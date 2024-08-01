from functools import partial
from typing import Dict, List, Optional

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

from ww.crud.resonator import get_resonator_names, get_resonator_skill_ids
from ww.model.template import (
    TemplateRowActionEnum,
    TemplateRowBuffEnum,
    TemplateRowBuffModel,
    TemplateRowBuffTypeEnum,
    TemplateRowEnum,
    TemplateRowModel,
)
from ww.ui.button import QDataPushButton
from ww.ui.table import QDraggableTableWidget


class QTemplateTabOutputMethodBuffTable(QDraggableTableWidget):
    def __init__(
        self,
        rows: int,
        columns: int,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
    ):
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=column_id_name,
            column_names=column_names,
        )

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == TemplateRowBuffEnum.TYPE.value:
            self.set_combobox(
                row, col, value, [e.value for e in TemplateRowBuffTypeEnum]
            )
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)


class QTemplateTabOutputMethodTable(QDraggableTableWidget):
    def __init__(self, ouput_methods: List[TemplateRowModel] = [TemplateRowModel()]):
        column_names = [e.value for e in TemplateRowEnum]

        rows = len(ouput_methods)
        columns = len(column_names)

        self.ouput_methods = ouput_methods

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

    def _init_column_width(self):
        for e in TemplateRowEnum:
            width = len(e.value) * 20 + 50
            col = self.column_names_table[e.value]
            self.setColumnWidth(col, width)

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.set_cell(None, row, col)

    def get_row(self, row: int) -> TemplateRowModel:
        return self.ouput_methods[row]

    def set_row(self, row: int, data: TemplateRowModel):
        if isinstance(data, TemplateRowModel):
            self.ouput_methods[row] = data
            for col in range(self.columnCount()):
                self.set_cell(None, row, col)

    def get_cell(self, row: int, col: int) -> str:
        cell = super().get_cell(row, col)
        if cell is not None:
            return cell
        return ""

    def set_cell(self, _: str, row: int, col: int):
        if self.column_names[col] == TemplateRowEnum.RESONATOR_NAME.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].resonator_name,
                [],
                getOptions=get_resonator_names,
            )
        elif self.column_names[col] == TemplateRowEnum.REAL_DMG_NO_CRIT.value:
            self.set_item(self.ouput_methods[row].real_dmg_no_crit, row, col)
        elif self.column_names[col] == TemplateRowEnum.REAL_DMG_CRIT.value:
            self.set_item(self.ouput_methods[row].real_dmg_crit, row, col)
        elif self.column_names[col] == TemplateRowEnum.SKILL_ID.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].skill_id,
                [],
                getOptions=partial(
                    get_resonator_skill_ids, self.ouput_methods[row].resonator_name
                ),
            )
        elif self.column_names[col] == TemplateRowEnum.ACTION.value:
            self.set_combobox(
                row,
                col,
                self.ouput_methods[row].action,
                [e.value for e in TemplateRowActionEnum],
            )
        elif self.column_names[col] == TemplateRowEnum.BONUS_BUFF.value:
            btn = QDataPushButton("+")
            btn.clicked.connect(partial(self.add_buff, row, btn))
            self.setCellWidget(row, col, btn)
        else:
            item = QTableWidgetItem("")
            self.setItem(row, col, item)

    def get_row_buff(self, row: int) -> List[List[str]]:
        data = []
        output_method = self.ouput_methods[row]

        for buff in output_method.buffs:
            # t = buff.type
            # if t is None:
            #     t = ""
            data.append([buff.name, buff.type, buff.value, buff.stack])
        if len(data) == 0:
            return [["", "", "", ""]]
        return data

    def set_row_buff(
        self, row: int, table: QDraggableTableWidget, btn: QDataPushButton
    ):
        data = table.get_data()
        buffs = []
        for d in data:
            buff = TemplateRowBuffModel(name=d[0], type=d[1], value=d[2], stack=d[3])
            buffs.append(buff)
        btn.set_data(buffs)
        self.ouput_methods[row].buffs = buffs

    def add_buff(self, row: int, btn: QDataPushButton):
        width = 800
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

        column_names = [e.value for e in TemplateRowBuffEnum]
        table = QTemplateTabOutputMethodBuffTable(
            len(data),
            len(column_names),
            data=data,
            column_names=column_names,
        )

        btns_layout = QHBoxLayout()
        ok_btn = QDataPushButton("OK")
        ok_btn.clicked.connect(partial(self.set_row_buff, row, table, btn))
        ok_btn.setFixedHeight(40)
        btns_layout.addStretch()
        btns_layout.addWidget(ok_btn)

        layout.addWidget(table)
        layout.addLayout(btns_layout)

        dialog.setLayout(layout)
        dialog.exec_()


class QTemplateOutputMethodTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_output_method_table = QTemplateTabOutputMethodTable()

        self.layout.addWidget(self.q_output_method_table)

        self.setLayout(self.layout)
