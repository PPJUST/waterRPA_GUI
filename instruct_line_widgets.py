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


class widget_instruct_line(QWidget):
    """整个指令控件组"""

    def __init__(self):
        super().__init__()
        # 初始化
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)

        self.toolButton_add_instruct = QToolButton()
        self.toolButton_add_instruct.setObjectName(u"toolButton_add_instruct")
        self.toolButton_add_instruct.setText('+')
        self.horizontalLayout.addWidget(self.toolButton_add_instruct)

        self.toolButton_delete_instruct = QToolButton()
        self.toolButton_delete_instruct.setObjectName(u"toolButton_delete_instruct")
        self.toolButton_delete_instruct.setText('-')
        self.horizontalLayout.addWidget(self.toolButton_delete_instruct)

        self.comboBox_select_command = QComboBox()
        self.comboBox_select_command.setObjectName(u"comboBox_select_command")
        self.comboBox_select_command.setMinimumWidth(80)
        self.comboBox_select_command.setMaximumWidth(80)
        self.horizontalLayout.addWidget(self.comboBox_select_command)

        self.widget_command_setting = QWidget()
        self.widget_command_setting.setObjectName(u"widget_command_setting")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_command_setting)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.widget_command_setting)

        # 连接槽函数
        self.comboBox_select_command.currentTextChanged.connect(self.select_command)

    def select_command(self, command: str):
        """选择命令"""
        value_widget = eval(f'{code_command_dict[command]}()')  # 利用字典获取不同命令对应的控件，并利用eval将字符串转换为对象
        layout = self.widget_command_setting.layout()  # 获取对应控件组中用于存放不同命令控件的控件的布局

        while layout.count():  # 先清空布局中的原有控件
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if value_widget:
            layout.addWidget(value_widget)


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
        if pic_file is None:
            pic_file, _ = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片文件(*.png *.jpg *.bmp)")
        if pic_file:
            self.label_show_pic.setText(pic_file)
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
        save_pic_file = r'region_screenshot.png'
        pyautogui.screenshot(save_pic_file, region=format_area)
        self.choose_pic(save_pic_file)

    # 备忘录 如果是勾选图片的话，后期修改图片路径为本地复制一份


class widget_command_input(QWidget):
    """输入指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_4 = QHBoxLayout(self)

        self.lineEdit_input = QLineEdit()
        self.lineEdit_input.setObjectName(u"lineEdit_input")
        self.lineEdit_input.setPlaceholderText("输入文本")
        self.horizontalLayout_4.addWidget(self.lineEdit_input)


class widget_command_wait(QWidget):
    """等待指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_5 = QHBoxLayout(self)

        self.doubleSpinBox_wait_second = QDoubleSpinBox()
        self.doubleSpinBox_wait_second.setObjectName(u"doubleSpinBox_wait_second")
        self.doubleSpinBox_wait_second.setMaximum(9999)
        self.horizontalLayout_5.addWidget(self.doubleSpinBox_wait_second)

        self.label = QLabel()
        self.label.setObjectName(u"label")
        self.label.setText('秒')
        self.horizontalLayout_5.addWidget(self.label)


class widget_command_scroll(QWidget):
    """滚轮指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_6 = QHBoxLayout(self)

        self.comboBox_scroll_direction = QComboBox()
        self.comboBox_scroll_direction.addItem("向上")
        self.comboBox_scroll_direction.addItem("向下")
        self.comboBox_scroll_direction.setObjectName(u"comboBox_scroll_direction")
        self.horizontalLayout_6.addWidget(self.comboBox_scroll_direction)

        self.spinBox_scroll_distance = QSpinBox()
        self.spinBox_scroll_distance.setObjectName(u"spinBox_scroll_distance")
        self.spinBox_scroll_distance.setMaximum(10000)
        self.spinBox_scroll_distance.setSingleStep(10)
        self.horizontalLayout_6.addWidget(self.spinBox_scroll_distance)


class widget_command_hotkey(QWidget):
    """模拟按键指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_7 = QHBoxLayout(self)

        self.lineEdit_hotkey = QLineEdit(self)
        self.lineEdit_hotkey.setObjectName(u"lineEdit_hotkey")
        self.lineEdit_hotkey.setPlaceholderText("多个热键用【空格】隔开，效果为同时按下")
        self.horizontalLayout_7.addWidget(self.lineEdit_hotkey)

        # 连接槽函数
        self.lineEdit_hotkey.textChanged.connect(self.text_changed)

    def text_changed(self):
        hotkey_split = self.lineEdit_hotkey.text().split(" ")
        wrong_key = [key for key in hotkey_split if key.lower() not in pyautogui_keyboard_keys and key.strip()]
        if wrong_key:
            self.lineEdit_hotkey.setStyleSheet("background: yellow;")  # 设置为黄色背景，提示用
        else:
            self.lineEdit_hotkey.setStyleSheet("")


class widget_command_custom(QWidget):
    """自定义指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_8 = QHBoxLayout(self)

        self.comboBox_custom_command = QComboBox()
        self.comboBox_custom_command.setObjectName(u"comboBox_custom_command")
        self.horizontalLayout_8.addWidget(self.comboBox_custom_command)


class DropLabel(QLabel):
    """自定义QLabel控件
    拖入图片文件到QLabel中，将QLabel的文本设置为【拖入的图片文件路径】，并且在QLabel上显示该图片
    并发送信号 signal_QLabel_dropped(str)
    注意：仅支持单个图片文件路径"""

    signal_QLabel_dropped = Signal(str)  # 发送获取的文件夹路径str信号

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)  # 设置可拖入

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()  # 获取路径
            if os.path.isfile(path) and filetype.is_image(path):
                self.setText(path)
                pixmap = QPixmap(path)
                resize = calculate_resize(self.size(), pixmap.size())
                pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
                self.setPixmap(pixmap)
                self.signal_QLabel_dropped.emit(path)


def _test_widget():
    # 测试显示效果
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication([])
    window = QWidget()

    # --------------
    test = widget_command_custom()
    # -------------

    layout = QVBoxLayout()
    layout.addWidget(test)

    window.setLayout(layout)

    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
