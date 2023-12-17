from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandKeyRelease(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('释放')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_key = QLineEdit()
        self.lineEdit_key.setPlaceholderText('仅支持指定名称的单键')
        if default_key:
            self.lineEdit_key.setText(default_key)
        self.horizontalLayout.addWidget(self.lineEdit_key)

        self.label_3 = QLabel()
        self.label_3.setText('键')
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
        self.lineEdit_key.textChanged.connect(self.check_args)
        self.lineEdit_key.textChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        key = args_dict['key']
        self.lineEdit_key.setText(key)

    def check_args(self):
        """检查参数规范"""
        key = self.lineEdit_key.text().strip()
        if key.lower() not in pyautogui_keyboard_keys:
            self.args_dict['args_all_right'] = False
            self.lineEdit_key.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.lineEdit_key.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        key = self.lineEdit_key.text().strip()
        self.args_dict['key'] = key

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandKeyRelease()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
