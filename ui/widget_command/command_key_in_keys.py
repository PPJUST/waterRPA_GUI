from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandKeyInKeys(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('模拟键入')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_keys = QLineEdit()
        self.lineEdit_keys.setPlaceholderText('指定名称的键，以空格间隔')
        if default_keys:
            self.lineEdit_keys.setText(default_keys)
        self.horizontalLayout.addWidget(self.lineEdit_keys)

        self.label_3 = QLabel()
        self.label_3.setText('中的键，执行')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_presses = QSpinBox()
        self.spinBox_presses.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_presses.setValue(default_presses)
        self.horizontalLayout.addWidget(self.spinBox_presses)

        self.label_4 = QLabel()
        self.label_4.setText('次，每次执行间隔')
        self.horizontalLayout.addWidget(self.label_4)

        self.doubleSpinBox_interval = QDoubleSpinBox()
        self.doubleSpinBox_interval.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_interval.setMaximum(max_interval)
        self.doubleSpinBox_interval.setValue(default_interval)
        self.horizontalLayout.addWidget(self.doubleSpinBox_interval)

        self.label_5 = QLabel()
        self.label_5.setText('秒')
        self.horizontalLayout.addWidget(self.label_5)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_keys.textChanged.connect(self.check_args)
        self.lineEdit_keys.textChanged.connect(self.send_args)
        self.spinBox_presses.valueChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        keys = args_dict['keys']
        presses = args_dict['presses']
        interval = args_dict['interval']
        self.lineEdit_keys.setText(keys)
        self.spinBox_presses.setValue(presses)
        self.doubleSpinBox_interval.setValue(interval)

    def check_args(self):
        """检查参数规范"""
        keys_split = self.lineEdit_keys.text().split(" ")
        wrong_key = [key for key in keys_split if key.lower() not in pyautogui_keyboard_keys and key.strip()]
        if wrong_key:
            self.args_dict['args_all_right'] = False
            self.lineEdit_keys.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.lineEdit_keys.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        keys = self.lineEdit_keys.text()
        presses = self.spinBox_presses.value()
        interval = self.doubleSpinBox_interval.value()

        self.args_dict['keys'] = keys
        self.args_dict['presses'] = presses
        self.args_dict['interval'] = interval

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandKeyInKeys()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
