from functools import partial
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from ww.locale import ZhTwEnum, _
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget


def set_buttons(data: List[List[str]], button_names: List[str]):
    button_length = len(button_names)
    if button_length == 0:
        return
    for i in range(len(data)):
        data[i] = ["" for _ in range(button_length)] + data[i]


class _QDraggableDescriptionTableWidget(QDraggableTableWidget):

    def __init__(
        self,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
        button_names: List[str] = [_(ZhTwEnum.BUFF_DESCRIPTION_BTN)],
    ):
        self.button_names = button_names
        set_buttons(data, self.button_names)

        new_column_names = button_names + column_names
        super().__init__(
            len(data), len(new_column_names), data, column_id_name, new_column_names
        )


class QDraggableDescriptionDataFrameTableWidget(_QDraggableDescriptionTableWidget):

    def __init__(
        self,
        df: pd.DataFrame,
        column_id_name: str = None,
        button_names: List[str] = [_(ZhTwEnum.BUFF_DESCRIPTION_BTN)],
    ):
        super().__init__(
            data=df.values.tolist(),
            column_id_name=column_id_name,
            column_names=df.columns.values.tolist(),
            button_names=button_names,
        )

    def set_description(self, row: int, col: int, dialog: QDialog, text: QTextEdit):
        plain_text = text.toPlainText()
        self.set_cell(row, col, plain_text)
        dialog.done(1)

    def add_description(self):
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
        dialog.setWindowTitle("Wuthering Waves Buff Description")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(x0, y0, width, height)

        col = self.get_column_id(_(ZhTwEnum.BUFF_DESCRIPTION.value))
        description = self.get_cell(row, col)
        text_edit = QTextEdit()
        text_edit.setText(description)

        btns_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(
            partial(self.set_description, row, col, dialog, text_edit)
        )
        ok_btn.setFixedHeight(40)
        btns_layout.addStretch()
        btns_layout.addWidget(ok_btn)

        layout.addWidget(text_edit)
        layout.addLayout(btns_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_cell(self, row: int, col: int, value: str):
        if col < len(self.button_names):
            btn = QPushButton(self.button_names[col])
            btn.clicked.connect(self.add_description)
            self.setCellWidget(row, col, btn)
        else:
            super().set_cell(row, col, value)


class QDraggableTsvDescriptionTableWidget(QDraggableTsvTableWidget):

    def __init__(
        self,
        table: QDraggableTableWidget,
        tsv_fpath: Optional[Union[str, Path]] = None,
        button_names: List[str] = [_(ZhTwEnum.BUFF_DESCRIPTION_BTN)],
    ):
        self.button_names = button_names
        super().__init__(
            table,
            tsv_fpath=tsv_fpath,
            event_save_column_names=self.save_column_names,
            event_save_row=self.save_row,
            event_load=self.load_,
            event_load_column_names=self.load_column_names,
        )

    def save_column_names(self, column_names: List[str]) -> List[str]:
        return column_names[len(self.button_names) :]

    def save_row(self, row: List[str]) -> List[str]:
        return row[len(self.button_names) :]

    def load_(self, data: List[List[str]]) -> List[List[str]]:
        set_buttons(data, self.button_names)
        return data

    def load_column_names(self, column_names: List[str]) -> List[str]:
        return self.button_names + column_names
