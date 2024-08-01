from PySide2.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget

from ww.model.echoes import EchoListEnum
from ww.tables.echoes import EchoListTable
from ww.ui.developer.template.basic import QTemplateBasicTab
from ww.ui.developer.template.output_method import QTemplateOutputMethodTab

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


class QTemplateTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_load_btn = QPushButton("讀取模板ID")
        self.q_load_btn.clicked.connect(self.load)
        self.q_save_btn = QPushButton("存檔")
        self.q_save_btn.clicked.connect(self.save)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_load_btn)
        self.q_btns_layout.addWidget(self.q_save_btn)

        self.q_tabs = QTabWidget()
        # Basic
        self.q_template_basic_tab = QTemplateBasicTab()
        # Output method
        self.q_template_output_method_tab = QTemplateOutputMethodTab(
            self.q_template_basic_tab
        )

        self.q_tabs.addTab(self.q_template_basic_tab, "基本資料")
        self.q_tabs.addTab(self.q_template_output_method_tab, "輸出手法")

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_tabs)
        self.setLayout(self.layout)

    def load(self):
        self.q_template_output_method_tab.load()

    def save(self):
        ...
        # print(self.q_resonator_table.get_resonators())
