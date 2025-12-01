from typing import Dict, List

try:
    from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
    from PySide2.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
except ImportError:  # pragma: no cover - optional dependency
    QT_AVAILABLE = False
else:
    QT_AVAILABLE = True


def build_rows(current: Dict[str, List[dict]], history: Dict[str, List[List[dict]]]) -> List[dict]:
    rows: List[dict] = []
    for config, issues in current.items():
        for issue in issues:
            rows.append({"config_name": config, **issue})
    for config, batches in history.items():
        for batch in batches:
            for issue in batch:
                rows.append({"config_name": config, **issue})
    return rows


if QT_AVAILABLE:

    class IssueTableModel(QAbstractTableModel):
        headers = ["config", "owner", "action", "category", "count"]

        def __init__(self, data: List[dict]):
            super().__init__()
            self._data = data

        def rowCount(self, parent=QModelIndex()):  # noqa: N802
            return len(self._data)

        def columnCount(self, parent=QModelIndex()):  # noqa: N802
            return len(self.headers)

        def data(self, index, role=Qt.DisplayRole):  # noqa: N802
            if not index.isValid() or role != Qt.DisplayRole:
                return None
            issue = self._data[index.row()]
            column = self.headers[index.column()]
            if column == "config":
                return issue.get("config_name", "")
            return issue.get(column, "")

        def headerData(self, section, orientation, role=Qt.DisplayRole):  # noqa: N802
            if role == Qt.DisplayRole and orientation == Qt.Horizontal:
                return self.headers[section]
            return None


    def launch_gui(current: Dict[str, List[dict]], history: Dict[str, List[List[dict]]]):
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle("LogScope Summary")
        layout = QVBoxLayout()

        table = QTableView()
        table.setModel(IssueTableModel(build_rows(current, history)))
        layout.addWidget(table)
        window.setLayout(layout)
        window.resize(900, 500)
        window.show()
        return app.exec_()

else:

    def launch_gui(current: Dict[str, List[dict]], history: Dict[str, List[List[dict]]]):  # type: ignore[misc]
        raise RuntimeError("PySide2 is required to launch the GUI")
