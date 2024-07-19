from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QHBoxLayout,
    QInputDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class QDraggableTableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTableWidget.InternalMove)
        self.setSelectionBehavior(QTableWidget.SelectRows)

        # Connect context menu for vertical header
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(
            self.show_header_context_menu
        )

    def drop_event(self, event):
        source = event.source()
        if source == self:
            selected_rows = self.selectionModel().selectedRows()
            source_row = selected_rows[0].row()

            target_row = self.rowAt(event.pos().y())
            if target_row == -1:
                target_row = self.rowCount() - 1

            self.insertRow(target_row)
            for column in range(self.columnCount()):
                self.setItem(target_row, column, self.takeItem(source_row, column))

            if target_row < source_row:
                source_row += 1

            self.removeRow(source_row)
            event.accept()
        else:
            super().drop_event(event)

    def show_header_context_menu(self, position):
        header = self.verticalHeader()
        row = header.logicalIndexAt(position)

        menu = QMenu()
        add_above_action = QAction("Add rows above", self)
        add_below_action = QAction("Add rows below", self)
        delete_selected_rows_action = QAction("Delete selected rows", self)
        menu.addAction(add_above_action)
        menu.addAction(add_below_action)
        menu.addAction(delete_selected_rows_action)

        add_above_action.triggered.connect(
            lambda: self._row_index_ctx_add_rows_above(row)
        )
        add_below_action.triggered.connect(
            lambda: self._row_index_ctx_add_rows_below(row)
        )
        delete_selected_rows_action.triggered.connect(
            self._row_index_ctx_delete_selected_rows
        )

        menu.exec_(header.viewport().mapToGlobal(position))

    def _row_index_ctx_fill_row(self, row):
        pass

    def _row_index_ctx_add_rows(self, row):
        num_rows, ok = QInputDialog.getInt(
            self, "Number of Rows", "Enter number of rows to add:", 1, 1
        )
        if ok:
            for _ in range(num_rows):
                self.insertRow(row)
                self._row_index_ctx_fill_row(row)

    def _row_index_ctx_add_rows_above(self, row):
        self._row_index_ctx_add_rows(row)

    def _row_index_ctx_add_rows_below(self, row):
        self._row_index_ctx_add_rows(row + 1)

    def _row_index_ctx_delete_selected_rows(self):
        selected_rows = sorted(set(index.row() for index in self.selectedIndexes()))
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "No rows selected to remove.")
            return

        confirmation = QMessageBox.question(
            self,
            "Remove Rows",
            f"Are you sure you want to remove {len(selected_rows)} row(s)?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            for row in reversed(selected_rows):
                self.removeRow(row)
