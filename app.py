import sys

from PySide2.QtWidgets import QApplication, QWidget

from ww.commands.custom.resonators.calc import get_df
from ww.ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
