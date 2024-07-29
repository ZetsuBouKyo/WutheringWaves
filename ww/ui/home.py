import sys
from functools import partial

from PySide2.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable


class QHomeTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.q_github_layout = QHBoxLayout()
        self.q_github_label = QLabel()
        self.q_github_label.setText("Github")
        self.q_github_link_label = QLabel()
        self.q_github_link_label.setText(
            '<a href="https://github.com/ZetsuBouKyo/WutheringWaves">Link</a>'
        )
        self.q_github_link_label.setOpenExternalLinks(True)
        self.q_github_layout.addWidget(self.q_github_label)
        self.q_github_layout.addWidget(self.q_github_link_label)
        self.q_github_layout.addStretch()

        self.q_twitch_layout = QHBoxLayout()
        self.q_twitch_label = QLabel()
        self.q_twitch_label.setText("Twitch")
        self.q_twitch_link_label = QLabel()
        self.q_twitch_link_label.setText(
            '<a href="https://www.twitch.tv/zetsuboukyo">Link</a>'
        )
        self.q_twitch_link_label.setOpenExternalLinks(True)
        self.q_twitch_layout.addWidget(self.q_twitch_label)
        self.q_twitch_layout.addWidget(self.q_twitch_link_label)
        self.q_twitch_layout.addStretch()

        self.layout.addLayout(self.q_github_layout)
        self.layout.addLayout(self.q_twitch_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)
