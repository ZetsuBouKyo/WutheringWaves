import sys
from functools import partial

import mistune
from PySide2.QtCore import QSize, QUrl
from PySide2.QtGui import QDesktopServices, QIcon
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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ww.crud.docs import get_home_html
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable

ICON_GITHUB_PATH = "./assets/mdi--github.svg"
ICON_TWITCH_PATH = "./assets/mdi--twitch.svg"


class QHomeTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.q_icons_layout = QHBoxLayout()
        self.q_github_btn = self.get_q_icon(
            ICON_GITHUB_PATH, "https://github.com/ZetsuBouKyo/WutheringWaves"
        )
        self.q_twitch_btn = self.get_q_icon(
            ICON_TWITCH_PATH, "https://www.twitch.tv/zetsuboukyo"
        )
        self.q_icons_layout.addStretch()
        self.q_icons_layout.addWidget(self.q_github_btn)
        self.q_icons_layout.addWidget(self.q_twitch_btn)

        self.q_text_layout = QVBoxLayout()
        self.q_text = QTextEdit()
        self.q_text.setAcceptRichText(True)
        self.q_text.setHtml(get_home_html())
        self.q_text_layout.addWidget(self.q_text)

        self.layout.addLayout(self.q_icons_layout)
        self.layout.addLayout(self.q_text_layout)

        self.setLayout(self.layout)

    def get_q_icon(self, icon_path: str, url: str) -> QPushButton:
        btn = QPushButton()
        btn.clicked.connect(partial(self.open_url, url))
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(50, 50))
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: white;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(220,220,220);
            }
        """
        )
        return btn

    def open_url(self, url):
        url = QUrl(url)
        QDesktopServices.openUrl(url)
