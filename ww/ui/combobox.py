from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox


class QCustomComboBox(QComboBox):
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrollWidget = scrollWidget
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        # if self.hasFocus() and self.isVisible():
        #     return super().wheelEvent(*args, **kwargs)
        if self.scrollWidget is not None:
            return self.scrollWidget.wheelEvent(*args, **kwargs)
