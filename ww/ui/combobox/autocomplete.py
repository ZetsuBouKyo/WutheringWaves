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
        self.model.setStringList(new_options)

    def wheelEvent(self, *args, **kwargs):
        # if self.hasFocus() and self.isVisible():
        #     return super().wheelEvent(*args, **kwargs)
        if self.scrollWidget is not None:
            return self.scrollWidget.wheelEvent(*args, **kwargs)

    def showPopup(self):
        if self.getOptions is not None:
            text = self.currentText()

            new_options = self.getOptions()
            if "" not in new_options:
                new_options = [""] + new_options
            new_options_to_add = []
            for option in new_options:
                if option not in self._option:
                    new_options_to_add.append(option)
            for option in new_options_to_add:
                self._option.append(option)
                self.addItem(option)

        super().showPopup()
