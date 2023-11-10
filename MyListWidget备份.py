class MyListWidget(QListWidget):
    itemMoved = Signal()

    def __init__(self, parent=None):
        super(MyListWidget, self).__init__(parent)

    def dropEvent(self, event):
        super(MyListWidget, self).dropEvent(event)
        self.itemMoved.emit()