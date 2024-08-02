from pathlib import Path

from PySide2.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.crud.template import TEMPLATE_HOME_PATH
from ww.model.echoes import EchoListEnum
from ww.model.template import TemplateModel
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
        template_id = self.q_template_basic_tab.get_template_id()
        template_id = template_id.strip()
        if template_id == "":
            QMessageBox.warning(self, "警告", "模板ID不該是空值。")
            return
        template_fname = f"{template_id}.json"
        template_path = Path(TEMPLATE_HOME_PATH) / template_fname

        if template_path.exists():
            confirmation = QMessageBox.question(
                self,
                "檔案已存在",
                f"你確定要覆蓋檔案'{template_fname}'？",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirmation == QMessageBox.No:
                return

        test_resonator_ids = self.q_template_basic_tab.get_test_resonator_ids()
        monster_id = self.q_template_basic_tab.get_monster_id()
        description = self.q_template_basic_tab.get_description()
        resonators = self.q_template_basic_tab.get_resonators()
        rows = self.q_template_output_method_tab.get_rows()
        template_data = TemplateModel(
            id=template_id,
            test_resonator_id_1=test_resonator_ids[0],
            test_resonator_id_2=test_resonator_ids[1],
            test_resonator_id_3=test_resonator_ids[2],
            monster_id=monster_id,
            description=description,
            resonators=resonators,
            rows=rows,
        )
        print(template_data)
