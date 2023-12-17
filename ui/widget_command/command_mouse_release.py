from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandMouseRelease(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_5 = QLabel()
        self.label_5.setText('释放')
        self.horizontalLayout.addWidget(self.label_5)

        self.comboBox_button = QComboBox()
        self.comboBox_button.addItems(['左键', '右键', '中键'])
        self.comboBox_button.setCurrentText(default_button)
        self.horizontalLayout.addWidget(self.comboBox_button)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_button.currentTextChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        button = args_dict['button']
        self.comboBox_button.setCurrentText(button)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        button = self.comboBox_button.currentText()
        self.args_dict['button'] = button

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMouseRelease()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
