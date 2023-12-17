"""自定义listwidget控件"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget


class MovedListWidget(QListWidget):
    itemMoved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)


    def dropEvent(self, event):
        super().dropEvent(event)
        self.itemMoved.emit()
