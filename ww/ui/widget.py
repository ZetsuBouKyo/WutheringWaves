from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget


class ScrollableWidget(QWidget):
    def __init__(self, widget: QWidget):
        super().__init__()

        # Create a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)

        # Set the QScrollArea as the main layout of the main widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
