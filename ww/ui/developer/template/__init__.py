from pathlib import Path

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.crud.template import (
    TEMPLATE_HOME_PATH,
    get_template,
    get_template_path,
    save_template,
)
from ww.model.echoes import EchoListEnum
from ww.model.template import TemplateModel, TemplateRowModel
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

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setMinimum(0)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_label = QLabel("")
        self.q_progress_label.setFixedWidth(150)
        self.q_calculate_btn = QPushButton("計算")
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_save_btn = QPushButton("存檔")
        self.q_save_btn.clicked.connect(self.save)
        self.q_load_btn = QPushButton("讀取")
        self.q_load_btn.setToolTip("讀取選取的模板ID")
        self.q_load_btn.clicked.connect(self.load)
        self.q_delete_btn = QPushButton("刪除")
        self.q_delete_btn.setToolTip("刪除選取的模板ID")
        self.q_delete_btn.clicked.connect(self.delete)

        self.q_btns_layout.addWidget(self.q_progress_bar)
        self.q_btns_layout.addWidget(self.q_progress_label)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_calculate_btn)
        self.q_btns_layout.addWidget(self.q_save_btn)
        self.q_btns_layout.addWidget(self.q_load_btn)
        self.q_btns_layout.addWidget(self.q_delete_btn)

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

    def reset_progress_bar(self):
        self.q_progress_bar.setValue(0.0)
        self.q_progress_label.setText("")

    def calculate(self):
        self.q_template_output_method_tab.calculate()

    def save(self):
        self.q_progress_bar.setValue(0.0)
        self.q_progress_label.setText("存檔中...")

        template_id = self.q_template_basic_tab.get_template_id()
        template_id = template_id.strip()
        if template_id == "":
            QMessageBox.warning(self, "警告", "模板ID不該是空值。")
            return
        template_fname = f"{template_id}.json"
        template_path = Path(TEMPLATE_HOME_PATH) / template_fname

        self.q_progress_bar.setValue(10.0)

        if template_path.exists():
            confirmation = QMessageBox.question(
                self,
                "檔案已存在",
                f"你確定要覆蓋檔案'{template_fname}'?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirmation == QMessageBox.No:
                self.reset_progress_bar()
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

        self.q_progress_bar.setValue(20.0)

        save_template(template_id, template_data)

        self.q_progress_bar.setValue(100.0)
        self.q_progress_label.setText("存檔完成。")

    def load(self):
        template_id = self.q_template_basic_tab.get_template_id()
        template = get_template(template_id)

        if template is None:
            QMessageBox.warning(self, "警告", "請選擇要讀取的模板ID。")
            return

        self.reset_progress_bar()

        if len(template.rows) == 0:
            template.rows.append(TemplateRowModel())

        self.q_template_basic_tab.load(template)
        self.q_template_output_method_tab.load(template.rows)

    def delete(self):
        template_id = self.q_template_basic_tab.get_template_id()
        if not template_id:
            QMessageBox.warning(self, "警告", "請選擇要刪除的模板ID。")
            return

        self.reset_progress_bar()

        confirmation = QMessageBox.question(
            self,
            "刪除",
            f"你確定要刪除模板 '{template_id}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.No:
            return

        template_path = get_template_path(template_id)
        if not template_path.is_dir() and template_path.exists():
            template_path.unlink()
            self.q_template_basic_tab.reset_template_id()
