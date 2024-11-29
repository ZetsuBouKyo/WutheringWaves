from copy import deepcopy

from PySide2.QtCore import QStringListModel, Qt
from PySide2.QtWidgets import QComboBox, QCompleter


class QAutoCompleteComboBox(QComboBox):
    def __init__(
        self,
        *args,
        scrollWidget=None,
        getOptions=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.getOptions = getOptions
        self.scrollWidget = scrollWidget

        self.setEditable(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self.model = QStringListModel()
        self.completer = QCompleter(self.model, self)
        self.setCompleter(self.completer)
        self.currentTextChanged.connect(self.update_completer)
        self.completer.setFilterMode(Qt.MatchContains)

        self._option = []

    def update_completer(self):
        if self.getOptions is not None:
            new_options = self.getOptions()
        else:
            new_options = [self.itemText(i) for i in range(self.count())]

        if new_options is None:
            return
        self.model.setStringList(new_options)

    def clear(self):
        super().clear()
        self._option = []

    def wheelEvent(self, *args, **kwargs):
        # if self.hasFocus() and self.isVisible():
        #     return super().wheelEvent(*args, **kwargs)
        if self.scrollWidget is not None:
            return self.scrollWidget.wheelEvent(*args, **kwargs)

    def showPopup(self):
        text = deepcopy(self.currentText())
        if self.getOptions is not None:

            new_options = self.getOptions()

            self.clear()
            if new_options is not None:
                for i, option in enumerate(new_options):
                    self.addItem(option, option)
                    self.setItemData(i, option, Qt.ToolTipRole)

        self.setCurrentText(text)

        super().showPopup()
