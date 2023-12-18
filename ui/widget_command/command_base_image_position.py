import os

import filetype
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from module.function_config import *
from ui import widget_screenshot


class DropLabel(QLabel):
    """自定义QLabel控件
    拖入【文件夹】/【文件】到QLabel中后，发送所有拖入路径的list信号
    发送信号 signal_dropped(list)"""
    signal_dropped = Signal(str)  # 发送拖入的所有路径list

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path_list = [url.toLocalFile() for url in urls]  # 获取多个文件的路径的列表
            first_path = drop_path_list[0]
            if os.path.isfile(first_path) and filetype.is_image(first_path):
                self.signal_dropped.emit(first_path)


class HBoxLayoutGroup1(QHBoxLayout):
    """组1"""
    signal_args_changed = Signal()  # 值变更后发送信号

    def __init__(self):
        super().__init__()
        """
        设置ui
        """
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

        """
        设置槽函数
        """
        self.toolButton_choose_pic.clicked.connect(self.choose_pic)
        self.toolButton_screenshot.clicked.connect(self.screenshot)
        self.label_show_pic.signal_dropped.connect(self.drop_image)
        # 设置值变更的信号
        self.label_show_pic.signal_dropped.connect(self.args_changed)
        self.doubleSpinBox_duration.valueChanged.connect(self.args_changed)
        self.comboBox_find_model.currentTextChanged.connect(self.args_changed)

    def args_changed(self):
        """值变更后发送信号"""
        self.signal_args_changed.emit()

    def drop_image(self, image_path):
        """响应拖入图片的信号"""
        self.choose_pic(image_path)

    def choose_pic(self, image_path=None):
        """弹出文件对话框选择图片，并设置label属性
        可传入image_path参数来跳过对话框"""
        if not image_path:
            image_path, _ = QFileDialog.getOpenFileName(self.parentWidget(), "选择图片", "/",
                                                        "图片文件(*.png *.jpg *.bmp)")

        if image_path:
            self.label_show_pic.setProperty('image_path', image_path)
            pixmap = QPixmap(image_path)
            resize = calculate_resize(self.label_show_pic.size(), pixmap.size())
            pixmap = pixmap.scaled(resize)
            self.label_show_pic.setPixmap(pixmap)

        self.args_changed()  # 发送信号

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


class HBoxLayoutGroup2(QHBoxLayout):
    """组2"""
    signal_args_changed = Signal()  # 值变更后发送信号

    def __init__(self):
        super().__init__()
        """设置ui"""
        self.label_5 = QLabel()
        self.label_5.setText('并点击')
        self.addWidget(self.label_5)

        self.comboBox_button = QComboBox()
        self.comboBox_button.addItems(['左键', '右键', '中键'])
        self.comboBox_button.setCurrentText(default_button)
        self.addWidget(self.comboBox_button)

        self.spinBox_clicks = QSpinBox()
        self.spinBox_clicks.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_clicks.setValue(default_clicks)
        self.spinBox_clicks.setMinimum(1)
        self.spinBox_clicks.setMaximum(max_clicks)
        self.addWidget(self.spinBox_clicks)

        self.label_6 = QLabel()
        self.label_6.setText('次，每次点击间隔')
        self.addWidget(self.label_6)

        self.doubleSpinBox_interval = QDoubleSpinBox()
        self.doubleSpinBox_interval.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_interval.setMaximum(max_interval)
        self.doubleSpinBox_interval.setValue(default_interval)
        self.addWidget(self.doubleSpinBox_interval)

        self.label_7 = QLabel()
        self.label_7.setText('秒')
        self.addWidget(self.label_7)

        """
        设置槽函数
        """
        # 设置值变更的信号
        self.comboBox_button.currentTextChanged.connect(self.args_changed)
        self.spinBox_clicks.valueChanged.connect(self.args_changed)
        self.doubleSpinBox_interval.valueChanged.connect(self.args_changed)

    def args_changed(self):
        """值变更后发送信号"""
        self.signal_args_changed.emit()


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = HBoxLayoutGroup1()
    # -------------
    window.setLayout(test)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
