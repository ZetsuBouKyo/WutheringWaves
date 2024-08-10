from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Union

import pandas as pd

from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget


class _QDraggableButtonTableWidget(QDraggableTableWidget):

    def __init__(
        self,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
        button_names: List[str] = [],
    ):
        self.button_names = button_names
        self.set_buttons(data, self.button_names)

        new_column_names = button_names + column_names
        super().__init__(
            len(data), len(new_column_names), data, column_id_name, new_column_names
        )

    def set_buttons(self, data: List[List[str]], button_names: List[str]):
        button_length = len(button_names)
        if button_length == 0:
            return
        for i in range(len(data)):
            data[i] = ["" for _ in range(button_length)] + data[i]


class QDraggableButtonDataFrameTableWidget(_QDraggableButtonTableWidget):

    def __init__(
        self,
        df: pd.DataFrame,
        column_id_name: str = None,
        button_names: List[str] = [],
    ):
        super().__init__(
            data=df.values.tolist(),
            column_id_name=column_id_name,
            column_names=df.columns.values.tolist(),
            button_names=button_names,
        )


class QDraggableTsvButtonTableWidget(QDraggableTsvTableWidget):

    def __init__(
        self,
        table: QDraggableTableWidget,
        tsv_fpath: Optional[Union[str, Path]] = None,
        event_load_before: Callable[[], None] = None,
        event_load_after: Callable[[], None] = None,
        event_save_after: Callable[[], None] = None,
        event_save_row_before: Callable[[int], None] = None,
        button_names: List[str] = [],
    ):
        self.button_names = button_names
        super().__init__(
            table,
            tsv_fpath=tsv_fpath,
            event_load_before=event_load_before,
            event_load_after=event_load_after,
            event_save_after=event_save_after,
            event_save_row_before=event_save_row_before,
        )

    def set_new_data(
        self, ids: Dict[str, int], dup_ids: Set[str], data: List[List[str]]
    ):
        for row in range(self._table.rowCount()):
            if self._event_save_row_before is not None:
                self._event_save_row_before(row)

            _new_data_row = ["" for _ in range(self._table.columnCount())]
            for col in range(self._table.columnCount()):
                _new_data_row[col] = self._table.get_cell(row, col)

            id_col = self._table.get_column_id(self._table.column_id_name)
            id = self._table.get_row_id(_new_data_row)
            if id in ids:
                dup_ids.add(str(ids[id] + 1))
                dup_ids.add(str(row + 1))
            if id != "":
                ids[id] = row

            if id is not None:
                _new_data_row[id_col] = id

            data.append(_new_data_row[len(self.button_names) :])

            self._progress_bar_update_row()
