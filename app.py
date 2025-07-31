import sys

from PySide2.QtWidgets import QApplication

from ww.ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget {
            background-color: black;
            color: white;
        }

        QLineEdit, QTextEdit {
            background-color: #333333;
            color: white;
            border: 1px solid #555;
        }

        QLabel {
            background-color: transparent;
            color: white;
        }

        QPushButton {
            background-color: #444;
            color: white;
            border: 1px solid #666;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #555;
        }

        /* Tab */
        QTabWidget::pane {
            border: 1px solid #666;
            background: black;
        }
        QTabBar::tab {
            background: #333;
            color: white;
            padding: 8px;
            border: 1px solid #666;
            border-bottom: none;
            min-width: 80px;
        }
        QTabBar::tab:selected {
            background: #222;
            font-weight: bold;
            border-bottom: 2px solid #222;
        }
        QTabBar::tab:hover {
            background: #444;
        }

        /* Table */
        QTableWidget {
            background-color: #111;
            color: white;
            gridline-color: #444;
            border: 1px solid #666;
            selection-background-color: #444;
            selection-color: white;
        }
        QHeaderView::section {
            background-color: #222;
            color: white;
            padding: 4px;
            border: 1px solid #444;
        }
        QTableCornerButton::section {
            background-color: #222;
            border: 1px solid #444;
        }
        QScrollBar:vertical {
            background: #222;
            width: 10px;
        }
        QScrollBar:horizontal {
            height: 10px;
            background: #222;
        }
        QScrollBar::handle {
            background: #555;
            border-radius: 4px;
        }
        QScrollBar::handle:hover {
            background: #666;
        }

        /* Combobox */
        QComboBox {
            background-color: #222;
            color: white;
            border: 1px solid #555;
            padding: 4px;
        }
        QComboBox:hover {
            background-color: #333;
        }
        QComboBox QAbstractItemView {
            background-color: #111;
            color: white;
            border: 1px solid #555;
            selection-background-color: #444;
            selection-color: white;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #555;
            background-color: #222;
        }
        QComboBox::down-arrow {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid white;
            margin-right: 6px;
        }

        QProgressBar {
            background-color: #222;
            border: 1px solid #444;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #555;
        }
        """
    )
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
