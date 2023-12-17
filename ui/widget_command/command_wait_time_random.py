from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandWaitTimeRandom(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setText('随机等待')
        self.horizontalLayout.addWidget(self.label)

        self.doubleSpinBox_wait_time_min = QDoubleSpinBox()
        self.doubleSpinBox_wait_time_min.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_wait_time_min.setMaximum(9999.99)
        self.doubleSpinBox_wait_time_min.setValue(default_wait_time_min)
        self.horizontalLayout.addWidget(self.doubleSpinBox_wait_time_min)

        self.label_2 = QLabel()
        self.label_2.setText('~')
        self.horizontalLayout.addWidget(self.label_2)

        self.doubleSpinBox_wait_time_max = QDoubleSpinBox()
        self.doubleSpinBox_wait_time_max.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_wait_time_max.setMaximum(9999.99)
        self.doubleSpinBox_wait_time_max.setValue(default_wait_time_max)
        self.horizontalLayout.addWidget(self.doubleSpinBox_wait_time_max)

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
        self.doubleSpinBox_wait_time_min.valueChanged.connect(self.send_args)
        self.doubleSpinBox_wait_time_max.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        wait_time_min = args_dict['wait_time_min']
        wait_time_max = args_dict['wait_time_max']
        self.doubleSpinBox_wait_time_min.setValue(wait_time_min)
        self.doubleSpinBox_wait_time_max.setValue(wait_time_max)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        wait_time_min = self.doubleSpinBox_wait_time_min.value()
        wait_time_max = self.doubleSpinBox_wait_time_max.value()
        self.args_dict['wait_time_min'] = wait_time_min
        self.args_dict['wait_time_max'] = wait_time_max

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandWaitTimeRandom()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec()


if __name__ == "__main__":
    _test_widget()
