from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandMouseScroll(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_4 = QLabel()
        self.label_4.setText('使用滚轮')
        self.horizontalLayout.addWidget(self.label_4)

        self.comboBox_scroll_direction = QComboBox()
        self.comboBox_scroll_direction.addItems(['向上', '向下'])
        self.comboBox_scroll_direction.setCurrentText(default_scroll_direction)
        self.horizontalLayout.addWidget(self.comboBox_scroll_direction)

        self.label_5 = QLabel()
        self.label_5.setText('滚动')
        self.horizontalLayout.addWidget(self.label_5)

        self.spinBox_scroll_distance = QSpinBox()
        self.spinBox_scroll_distance.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_scroll_distance.setMaximum(9999)
        self.spinBox_scroll_distance.setValue(default_scroll_distance)
        self.horizontalLayout.addWidget(self.spinBox_scroll_distance)

        self.label_6 = QLabel()
        self.label_6.setText('像素距离')
        self.horizontalLayout.addWidget(self.label_6)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_scroll_direction.currentTextChanged.connect(self.send_args)
        self.spinBox_scroll_distance.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        scroll_direction = args_dict['scroll_direction']
        scroll_distance = args_dict['scroll_distance']
        self.comboBox_scroll_direction.setCurrentText(scroll_direction)
        self.spinBox_scroll_distance.setValue(scroll_distance)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        scroll_direction = self.comboBox_scroll_direction.currentText()
        scroll_distance = self.spinBox_scroll_distance.value()
        self.args_dict['scroll_direction'] = scroll_direction
        self.args_dict['scroll_distance'] = scroll_distance

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMouseScroll()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
