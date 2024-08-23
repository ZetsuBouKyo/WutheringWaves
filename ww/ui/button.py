from typing import Any, Optional

from PySide2.QtWidgets import QPushButton, QToolTip


class QDataPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None

    def set_data(self, data: Any):
        self._data = data

    def get_data(self) -> Optional[Any]:
        return self._data

    def enterEvent(self, event, *args, **kwargs):
        QToolTip.showText(event.globalPos(), self.toolTip(), self)
        super().enterEvent(event, *args, **kwargs)
