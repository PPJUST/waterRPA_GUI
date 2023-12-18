from PySide6.QtWidgets import *

from module.constant_default import *
from module.function_general import *


class CommandScreenshotFullscreen(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('全屏截图，保存为')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_pic_file = QLineEdit()
        self.lineEdit_pic_file.setPlaceholderText('输入文件名，如存在则覆盖')
        if default_screenshot_image_path:
            self.lineEdit_pic_file.setText(default_screenshot_image_path)
        self.horizontalLayout.addWidget(self.lineEdit_pic_file)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_pic_file.textChanged.connect(self.check_args)
        self.lineEdit_pic_file.textChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        save_screenshot_image_path = args_dict['screenshot_image_path']
        self.lineEdit_pic_file.setText(save_screenshot_image_path)

    def check_args(self):
        """检查参数规范"""
        pic_file = self.lineEdit_pic_file.text().strip()
        if not pic_file or not check_filename_feasible(pic_file):
            self.args_dict['args_all_right'] = False
            self.lineEdit_pic_file.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.lineEdit_pic_file.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        image_name = self.lineEdit_pic_file.text().strip()
        if image_name:
            if image_name.endswith('.png'):
                self.args_dict['screenshot_image_path'] = image_name
            else:
                self.args_dict['screenshot_image_path'] = f'{image_name}.png'

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandScreenshotFullscreen()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
