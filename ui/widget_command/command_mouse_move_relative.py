from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandMouseMoveRelative(QWidget):
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
        self.label_2.setText('秒，')
        self.horizontalLayout.addWidget(self.label_2)

        self.comboBox_direction = QComboBox()
        self.comboBox_direction.addItems(['向左', '向上', '向下', '向右'])
        self.comboBox_direction.setCurrentText(default_move_direction)
        self.horizontalLayout.addWidget(self.comboBox_direction)

        self.label_3 = QLabel()
        self.label_3.setText('移动')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_distance = QSpinBox()
        self.spinBox_distance.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_distance.setMaximum(max_move_distance)
        self.spinBox_distance.setSingleStep(50)
        self.spinBox_distance.setValue(default_move_distance)
        self.horizontalLayout.addWidget(self.spinBox_distance)

        self.label_3 = QLabel()
        self.label_3.setText('像素距离')
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
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)
        self.comboBox_direction.currentTextChanged.connect(self.send_args)
        self.spinBox_distance.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        duration = args_dict['duration']
        move_direction = args_dict['move_direction']
        move_distance = args_dict['move_distance']
        self.doubleSpinBox_duration.setValue(duration)
        self.comboBox_direction.setCurrentText(move_direction)
        self.spinBox_distance.setValue(move_distance)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        duration = self.doubleSpinBox_duration.value()
        move_direction = self.comboBox_direction.currentText()
        move_distance = self.spinBox_distance.value()
        self.args_dict['duration'] = duration
        self.args_dict['move_direction'] = move_direction
        self.args_dict['move_distance'] = move_distance

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMouseMoveRelative()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
