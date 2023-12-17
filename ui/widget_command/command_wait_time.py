from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandWaitTime(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('等待')
        self.horizontalLayout.addWidget(self.label_2)

        self.doubleSpinBox_wait_time = QDoubleSpinBox()
        self.doubleSpinBox_wait_time.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_wait_time.setMaximum(9999.99)
        self.doubleSpinBox_wait_time.setValue(default_wait_time)
        self.horizontalLayout.addWidget(self.doubleSpinBox_wait_time)

        self.label_3 = QLabel()
        self.label_3.setText('秒')
        self.horizontalLayout.addWidget(self.label_3)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.doubleSpinBox_wait_time.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        wait_time = args_dict['wait_time']
        self.doubleSpinBox_wait_time.setValue(wait_time)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        wait_time = self.doubleSpinBox_wait_time.value()
        self.args_dict['wait_time'] = wait_time

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandWaitTime()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec()


if __name__ == "__main__":
    _test_widget()
