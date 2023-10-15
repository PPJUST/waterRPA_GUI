"""
单个控件组内部的操作都在该模块实现
"""
import os

import filetype
import pyautogui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import qdialog_screenshot

"""
定义常量
"""
code_command_dict = {'': '',
                     '单击左键': 'widget_command_pic',
                     '双击左键': 'widget_command_pic',
                     '单击右键': 'widget_command_pic',
                     '输入文本': 'widget_command_input',
                     '等待时间': 'widget_command_wait',
                     '等待时间(随机)': 'widget_command_wait',
                     '滚动滚轮': 'widget_command_scroll',
                     '模拟按键': 'widget_command_hotkey',
                     '自定义命令': 'widget_command_custom'}  # 第一个元素留空，用于初始显示

pyautogui_keyboard_keys = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
                           '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                           '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                           'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback',
                           'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch',
                           'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal',
                           'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                           'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22',
                           'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul',
                           'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2',
                           'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                           'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9',
                           'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print',
                           'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select',
                           'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                           'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command',
                           'option', 'optionleft', 'optionright']


def calculate_resize(qsize_label: QSize, qsize_pic: QSize) -> QSize:
    """传入两个QSize大小，计算新的QSize
    用于将图片保持纵横比显示在QLabel上"""
    label_width = qsize_label.width()
    label_height = qsize_label.height()
    pic_width = qsize_pic.width()
    pic_height = qsize_pic.height()

    label_rate = label_width / label_height
    pic_rate = pic_width / pic_height

    if label_rate >= pic_rate:  # 符合则按高缩放
        resize_height = label_height
        resize_width = int(pic_width / pic_height * resize_height)
        resize = QSize(resize_width, resize_height)
    else:  # 否则按宽缩放
        resize_width = label_width
        resize_height = int(pic_height / pic_width * resize_width)
        resize = QSize(resize_width, resize_height)
    """
    后续操作说明
    pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
    self.label.setPixmap(pixmap)
    """

    return resize

def create_random_string(length: int):
    """生成一个指定长度的随机字符串（小写英文+数字）
    传参：length 字符串的长度
    返回值：生成的str"""
    import string
    import random

    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(characters, k=length))

    return random_string


class widget_command_pic(QWidget):
    """单击、双击、右键的图片指令设置"""

    def __init__(self):
        super().__init__()
        # 初始化
        self.horizontalLayout_3 = QHBoxLayout(self)

        self.label_show_pic = DropLabel()
        self.label_show_pic.setObjectName(u"label_show_pic")
        self.label_show_pic.setText('显示图片')
        self.horizontalLayout_3.addWidget(self.label_show_pic)

        self.toolButton_choose_pic = QToolButton()
        self.toolButton_choose_pic.setObjectName(u"toolButton_choose_pic")
        self.toolButton_choose_pic.setText('选择')
        self.horizontalLayout_3.addWidget(self.toolButton_choose_pic)

        self.toolButton_screenshot = QToolButton()
        self.toolButton_screenshot.setObjectName(u"toolButton_screenshot")
        self.toolButton_screenshot.setText('截图')
        self.horizontalLayout_3.addWidget(self.toolButton_screenshot)

        # 连接槽函数
        self.toolButton_choose_pic.clicked.connect(self.choose_pic)
        self.toolButton_screenshot.clicked.connect(self.screenshot)

    def choose_pic(self, pic_file=None):
        """弹出文件对话框选择图片"""
        if not pic_file:
            pic_file, _ = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片文件(*.png *.jpg *.bmp)")

        if pic_file:
            self.label_show_pic.setProperty('pic_path', pic_file)
            pixmap = QPixmap(pic_file)
            resize = calculate_resize(self.label_show_pic.size(), pixmap.size())
            pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
            self.label_show_pic.setPixmap(pixmap)

    def screenshot(self):
        """截屏"""
        print(self.sender().parentWidget())
        dialog = qdialog_screenshot.QDialogScreenshot()
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

        format_area = [x_start, y_start, x_end - x_start, y_end - y_start]
        print(f'截图区域 {format_area}')

        save_pic_file = f'config/{create_random_string(16)}.png'
        pyautogui.screenshot(save_pic_file, region=format_area)
        self.choose_pic(save_pic_file)

    # 备忘录 如果是勾选图片的话，后期修改图片路径为本地复制一份

