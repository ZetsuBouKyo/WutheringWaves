from PySide2.QtWidgets import QVBoxLayout, QWidget


class QTemplateHelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
