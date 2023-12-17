from PySide6.QtGui import *

from module.function_config import *
from ui import widget_screenshot


class HBoxLayoutGroup(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setText('匹配图片')
        self.addWidget(self.label)

        self.label_show_pic = DropLabel()
        self.label_show_pic.setText('拖入图片')
        self.label_show_pic.setFrameShape(QFrame.Box)
        self.label_show_pic.setFrameShadow(QFrame.Sunken)
        self.addWidget(self.label_show_pic)

        self.label_2 = QLabel()
        self.label_2.setText('，分别使用')
        self.addWidget(self.label_2)

        self.doubleSpinBox_duration = QDoubleSpinBox()
        self.doubleSpinBox_duration.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_duration.setMaximum(max_duration)
        self.doubleSpinBox_duration.setValue(default_duration)
        self.addWidget(self.doubleSpinBox_duration)

        self.label_3 = QLabel()
        self.label_3.setText('秒移动鼠标至')
        self.addWidget(self.label_3)

        self.comboBox_find_model = QComboBox()
        self.comboBox_find_model.addItems(['第一个', '全部'])
        self.comboBox_find_model.setCurrentText(default_mode_find_image)
        self.addWidget(self.comboBox_find_model)

        self.label_4 = QLabel()
        self.label_4.setText('匹配位置')
        self.addWidget(self.label_4)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.addWidget(self.line)

        self.toolButton_choose_pic = QToolButton()
        self.toolButton_choose_pic.setText('选图')
        self.addWidget(self.toolButton_choose_pic)

        self.toolButton_screenshot = QToolButton()
        self.toolButton_screenshot.setText('截图')
        self.addWidget(self.toolButton_screenshot)


class CommandMoveToPicPosition(QWidget):
    signal_args = Signal(dict)

    def __init__(self, set_layout=True):
        super().__init__()
        """
        ui设置
        """
        self.ui = HBoxLayoutGroup()
        if set_layout:  # 作为父类时不调用
            self.setLayout(self.ui)
        # 重新赋值控件对象
        self.toolButton_choose_pic = self.ui.toolButton_choose_pic
        self.toolButton_screenshot = self.ui.toolButton_screenshot
        self.label_show_pic = self.ui.label_show_pic
        self.doubleSpinBox_duration = self.ui.doubleSpinBox_duration
        self.comboBox_find_model = self.ui.comboBox_find_model

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.check_args()
        if set_layout:  # 作为父类时不调用
            self.send_args()

        """
        槽函数设置
        """
        self.toolButton_choose_pic.clicked.connect(self.choose_pic)
        self.toolButton_screenshot.clicked.connect(self.screenshot)
        self.label_show_pic.signal_dropped.connect(self.drop_image)
        self.label_show_pic.signal_dropped.connect(self.check_args)
        self.label_show_pic.signal_dropped.connect(self.send_args)
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)
        self.comboBox_find_model.currentTextChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        duration = args_dict['duration']
        mode_find_image = args_dict['mode_find_image']
        screenshot_image_path = args_dict['screenshot_image_path']
        self.doubleSpinBox_duration.setValue(duration)
        self.comboBox_find_model.setCurrentText(mode_find_image)

        if screenshot_image_path and os.path.exists(screenshot_image_path) and filetype.is_image(screenshot_image_path):
            self.choose_pic(screenshot_image_path)

    def drop_image(self, image_path):
        """响应拖入图片的信号"""
        self.choose_pic(image_path)

    def choose_pic(self, image_path=None):
        """弹出文件对话框选择图片，并设置label属性
        可传入image_path参数来跳过对话框"""
        if not image_path:
            image_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "/", "图片文件(*.png *.jpg *.bmp)")

        if image_path:
            self.label_show_pic.setProperty('image_path', image_path)
            pixmap = QPixmap(image_path)
            resize = calculate_resize(self.label_show_pic.size(), pixmap.size())
            pixmap = pixmap.scaled(resize)
            self.label_show_pic.setPixmap(pixmap)

            self.check_args()
            self.send_args()

    def screenshot(self):
        """截屏"""
        dialog = widget_screenshot.ScreenFrameSelectDialog()
        dialog.signal_screenshot_area.connect(dialog.close)  # 先关闭dialog再进行截图，防止将遮罩也截入
        dialog.signal_screenshot_area.connect(self.get_screenshot_area)
        dialog.exec_()

    def get_screenshot_area(self, screenshot_area: list):
        """获取截屏区域的信号"""
        x_start, y_start, x_end, y_end = screenshot_area
        if x_start > x_end:  # pyautogui的截图只支持正数，所以需要调换
            x_start, x_end = x_end, x_start
        if y_start > y_end:  # pyautogui的截图只支持正数，所以需要调换
            y_start, y_end = y_end, y_start

        format_area = (x_start, y_start, x_end - x_start, y_end - y_start)

        image_name = f'screenshot_{create_random_string(8)}.png'
        save_pic_file = os.path.normpath(os.path.join(os.getcwd(), screenshot_folder, image_name))
        pyautogui.screenshot(save_pic_file, region=format_area)

        self.choose_pic(save_pic_file)

    def check_args(self):
        """检查参数规范"""
        pic_file = self.label_show_pic.property('image_path')
        if not pic_file or not os.path.exists(pic_file) or not filetype.is_image(pic_file):
            self.args_dict['args_all_right'] = False
            self.label_show_pic.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.label_show_pic.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        mode_find_image = self.comboBox_find_model.currentText()
        duration = self.doubleSpinBox_duration.value()
        self.args_dict['mode_find_image'] = mode_find_image
        self.args_dict['duration'] = duration

        image_path_property = self.label_show_pic.property('image_path')
        screenshot_image_path = image_path_property if image_path_property else ''  # 不能是None
        if screenshot_image_path:
            self.args_dict['screenshot_image_path'] = screenshot_image_path

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMoveToPicPosition()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
