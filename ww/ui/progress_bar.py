from PySide2.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget

from ww.locale import ZhHantEnum, _


class QHProgressBar(QWidget):
    def __init__(self):
        super().__init__()

        self.q_progress_layout = QHBoxLayout()
        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setToolTip(_(ZhHantEnum.PROGRESS_BAR))
        self.q_progress_bar.setMinimum(0)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_label = QLabel("")
        self.q_progress_label.setFixedWidth(150)
        self.q_progress_layout.addStretch()
        self.q_progress_layout.addWidget(self.q_progress_label)
        self.q_progress_layout.addWidget(self.q_progress_bar)

        self.setLayout(self.q_progress_layout)

    def set(self, percentage: int, message: str):
        self.q_progress_bar.setValue(percentage)
        self.q_progress_label.setText(message)

    def set_percentage(self, percentage: int):
        self.q_progress_bar.setValue(percentage)

    def reset(self):
        self.set(0.0, "")
