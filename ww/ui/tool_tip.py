from PySide2.QtCore import QPoint, Qt
from PySide2.QtWidgets import QCompleter, QToolTip


class QToolTipCompleter(QCompleter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popup().setMouseTracking(True)
        self.popup().entered.connect(self.show_tooltip)

    def show_tooltip(self, index):
        item_text = self.model().data(index, Qt.DisplayRole)
        global_pos = self.popup().mapToGlobal(QPoint(0, 0))
        item_pos = self.popup().visualRect(index).topLeft()

        QToolTip.showText(global_pos + item_pos, item_text)
