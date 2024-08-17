from datetime import datetime

from PySide2.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget

from ww.locale import ZhTwEnum, _


class QHProgressBar(QWidget):
    def __init__(self):
        super().__init__()

        self.q_progress_layout = QHBoxLayout()
        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setToolTip(_(ZhTwEnum.PROGRESS_BAR))
        self.q_progress_bar.setMinimum(0)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_label = QLabel("")
        self.q_progress_layout.addWidget(self.q_progress_label)
        self.q_progress_layout.addStretch()
        self.q_progress_layout.addWidget(self.q_progress_bar)

        self.setLayout(self.q_progress_layout)

    def set(self, percentage: int, message: str):
        self.set_percentage(percentage)
        self.set_message(message)

    def set_message(self, message: str):
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        msg = f"[{now}] {message}"
        self.q_progress_label.setText(msg)

    def set_percentage(self, percentage: int):
        self.q_progress_bar.setValue(percentage)

    def reset(self):
        self.set(0.0, "")
