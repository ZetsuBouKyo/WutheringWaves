from copy import deepcopy
from typing import List

from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.layout import FlowLayout, clear_layout
from ww.ui.widget import ScrollableWidget


class QChipWidget(QWidget):

    def __init__(self, i: int, chip: str, parent):
        super().__init__()
        self._index = i
        self._chip = chip
        self._parent = parent

        self.layout = QHBoxLayout()

        self.q_delete_btn = QPushButton("✖")
        self.q_delete_btn.setFixedWidth(30)
        self.q_delete_btn.clicked.connect(self.delete)
        self.q_label = QLabel(chip)

        self.layout.addWidget(self.q_delete_btn)
        self.layout.addWidget(self.q_label)

        self.setLayout(self.layout)

    def delete(self):
        self._parent.delete_chip(self._index)


class QChipsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._chips = []

        self.layout = QVBoxLayout()

        self.flow_layout = FlowLayout()
        self.layout.addLayout(self.flow_layout)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def add_chip(self, chip: str):
        self._chips.append(chip)
        i = len(self._chips) - 1

        q_chip = QChipWidget(i, chip, self)
        self.flow_layout.addWidget(q_chip)

    def delete_chip(self, i: int):
        del self._chips[i]
        chips = deepcopy(self._chips)
        self._chip = []
        self.set_chips(chips)

    def get_chips(self) -> List[str]:
        return self._chips

    def set_chips(self, chips: List[str]):
        clear_layout(self.flow_layout)
        self._chips = chips
        for i, chip in enumerate(chips):
            q_chip = QChipWidget(i, chip, self)
            self.flow_layout.addWidget(q_chip)

    def reset(self):
        self._chips = []
        clear_layout(self.flow_layout)


class QInputChipsWidget(QWidget):
    def __init__(self, getOptions=None):
        super().__init__()
        self.layout = QVBoxLayout()

        # Input
        self.q_input_layout = QHBoxLayout()
        self.q_input = QAutoCompleteComboBox(getOptions=getOptions)
        self.q_input.setFixedWidth(200)
        self.q_input.setFixedHeight(40)
        self.q_add_btn = QPushButton("+")
        self.q_add_btn.setFixedWidth(40)
        self.q_add_btn.setFixedHeight(40)
        self.q_add_btn.clicked.connect(self.add_chip)
        self.q_input_layout.addWidget(self.q_input)
        self.q_input_layout.addWidget(self.q_add_btn)
        self.q_input_layout.addStretch()

        # Chips
        self.q_chips = QChipsWidget()
        self.q_scrollable_chips = ScrollableWidget(self.q_chips)

        self.layout.addLayout(self.q_input_layout)
        self.layout.addWidget(self.q_scrollable_chips)

        self.setLayout(self.layout)

    def add_chip(self):
        chip = self.q_input.currentText()
        if not chip:
            return
        self.q_chips.add_chip(chip)

    def add_chips(self, chips: List[str]):
        self.q_chips.set_chips(chips)

    def get_chips(self) -> List[str]:
        return self.q_chips.get_chips()

    def reset(self):
        self.q_chips.reset()
