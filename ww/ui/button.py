from typing import Any, Optional

from PySide2.QtWidgets import QPushButton


class QDataPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None

    def set_data(self, data: Any):
        self._data = data

    def get_data(self) -> Optional[Any]:
        return self._data
