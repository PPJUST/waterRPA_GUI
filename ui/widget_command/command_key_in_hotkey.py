from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandKeyInHotkey(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('使用')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_hotkeys = QLineEdit()
        self.lineEdit_hotkeys.setPlaceholderText('指定名称的键，以空格间隔')
        if default_hotkey:
            self.lineEdit_hotkeys.setText(default_hotkey)
        self.horizontalLayout.addWidget(self.lineEdit_hotkeys)

        self.label_3 = QLabel()
        self.label_3.setText('热键')
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
        self.lineEdit_hotkeys.textChanged.connect(self.check_args)
        self.lineEdit_hotkeys.textChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        hotkey = args_dict['hotkey']
        self.lineEdit_hotkeys.setText(hotkey)

    def check_args(self):
        """检查参数规范"""
        keys_split = self.lineEdit_hotkeys.text().split(" ")
        wrong_key = [key for key in keys_split if key.lower() not in pyautogui_keyboard_keys and key.strip()]
        if wrong_key:
            self.args_dict['args_all_right'] = False
            self.lineEdit_hotkeys.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.lineEdit_hotkeys.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        hotkey = self.lineEdit_hotkeys.text()
        self.args_dict['hotkeys'] = hotkey

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandKeyInHotkey()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
