from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QCompleter


class QCustomComboBox(QComboBox):

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

    def wheelEvent(self, *args, **kwargs):
        # if self.hasFocus() and self.isVisible():
        #     return super().wheelEvent(*args, **kwargs)
        if self.scrollWidget is not None:
            return self.scrollWidget.wheelEvent(*args, **kwargs)

    def showPopup(self):
        if self.getOptions is not None:
            text = self.currentText()
            self.clear()

            new_options = self.getOptions()
            try:
                new_options.remove(text)
            except ValueError:
                ...
            options = [text] + new_options
            self.addItems(options)
            completer = QCompleter(self.model())
            self.setCompleter(completer)

        super().showPopup()
