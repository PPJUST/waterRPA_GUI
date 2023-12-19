from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandMouseMoveAbsolute(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_1 = QLabel()
        self.label_1.setText('使用')
        self.horizontalLayout.addWidget(self.label_1)

        self.doubleSpinBox_duration = QDoubleSpinBox()
        self.doubleSpinBox_duration.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_duration.setMaximum(max_duration)
        self.doubleSpinBox_duration.setValue(default_duration)
        self.horizontalLayout.addWidget(self.doubleSpinBox_duration)

        self.label_2 = QLabel()
        self.label_2.setText('秒，移动至坐标轴 (X')
        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_x = QSpinBox()
        self.spinBox_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_x.setMaximum(max_x)
        self.spinBox_x.setValue(default_x)
        self.horizontalLayout.addWidget(self.spinBox_x)

        self.label_3 = QLabel()
        self.label_3.setText(', Y')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_y = QSpinBox()
        self.spinBox_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_y.setMaximum(max_y)
        self.spinBox_y.setValue(default_y)
        self.horizontalLayout.addWidget(self.spinBox_y)

        self.label_4 = QLabel()
        self.label_4.setText(')')
        self.horizontalLayout.addWidget(self.label_4)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)
        self.spinBox_x.valueChanged.connect(self.send_args)
        self.spinBox_y.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        duration = args_dict['duration']
        x = args_dict['x']
        y = args_dict['y']
        self.doubleSpinBox_duration.setValue(duration)
        self.spinBox_x.setValue(x)
        self.spinBox_y.setValue(y)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        duration = self.doubleSpinBox_duration.value()
        x = self.spinBox_x.value()
        y = self.spinBox_y.value()
        self.args_dict['duration'] = duration
        self.args_dict['x'] = x
        self.args_dict['y'] = y

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMouseMoveAbsolute()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
