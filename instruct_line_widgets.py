"""单个控件组内部的操作都在该模块实现"""

import os
from typing import Union

import filetype
import pyautogui
from PySide2.QtCore import Signal, QSize, Qt
from PySide2.QtGui import QDropEvent, QPixmap, QDragEnterEvent, QIcon
from PySide2.QtWidgets import QLabel, QWidget, QToolButton, QAbstractSpinBox, QHBoxLayout, QSpinBox, QComboBox, \
    QDoubleSpinBox, QLineEdit, QFrame, QFileDialog, QVBoxLayout, QApplication

import qdialog_screenshot
from constant_setting import default_args_dict, pyautogui_keyboard_keys, command_link_dict, icon_edit, \
    error_stylesheet_border


def check_filename_feasible(filename: str, replace: bool = False) -> Union[str, bool]:
    """检查文件名是否符合Windows规范
    传参:
    filename 仅文件名（不含路径）
    replace 是否替换非法字符"""
    # 官方文档：文件和文件夹不能命名为“.”或“..”，也不能包含以下任何字符: # % & * | \ : " < > ?/
    except_word = [':', '#', '%', '&', '*', '|', '\\', ':', '"', '<', '>', '?', '/']
    if not replace:  # 不替换时，仅检查
        # 检查.
        if filename[0] == '.':
            return False

        # 检查# % & * | \ : " < > ?/

        for key in except_word:
            if key in filename:
                return False
        return True
    else:
        for word in except_word:
            filename = filename.replace(word, '')
        while filename[0] == '.':
            filename = filename[1:]

        return filename.strip()


def convert_args_dict(args_dict_config: dict):
    """转换config中的args_dict为widget的对应格式"""
    args_dict_convert = {}
    for key in args_dict_config:
        value_str = args_dict_config[key]
        try:
            value = eval(f'{value_str}')  # 转换文本为对应格式
        except NameError:  # 如果原本就是str，则使用eval后会报错
            value = value_str
        except:
            value = value_str

        # 处理特殊的几个
        if key == 'distance' and value < 0:
            args_dict_convert['default_direction'] = '向下'
            args_dict_convert[f'default_{key}'] = -value
            continue
        if key == 'wait_time' and type(value) is tuple:
            args_dict_convert['default_wait_time_min'] = value[0]
            args_dict_convert['default_wait_time_max'] = value[1]
            continue
        if key == 'command_type':
            args_dict_convert[key] = value
            continue
        if key == 'message' or key == 'key':
            if type(value) is not str:
                value = str(value)
            args_dict_convert[f'default_{key}'] = value
            continue
        if key == 'hotkeys' or key == 'keys':
            args_dict_convert[f'default_{key}'] = ' '.join(value)
            continue


        # 其余的都是原名前+default_
        args_dict_convert[f'default_{key}'] = value

    return args_dict_convert


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
                self.setProperty('pic_path', path)
                pixmap = QPixmap(path)
                resize = calculate_resize(self.size(), pixmap.size())
                pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
                self.setPixmap(pixmap)
                self.signal_QLabel_dropped.emit(path)


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


class WidgetInstructLine(QWidget):
    """整个指令控件组"""
    signal_send_args = Signal(dict)  # 子控件信号的中转发送

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)

        self.toolButton_state = QToolButton()
        self.toolButton_state.setText('状态')
        self.toolButton_state.setAutoRaise(True)
        self.toolButton_state.setIcon(QIcon(icon_edit))

        self.horizontalLayout.addWidget(self.toolButton_state)

        self.toolButton_add_instruct = QToolButton()
        self.toolButton_add_instruct.setText('+')
        self.horizontalLayout.addWidget(self.toolButton_add_instruct)

        self.toolButton_delete_instruct = QToolButton()
        self.toolButton_delete_instruct.setText('-')
        self.horizontalLayout.addWidget(self.toolButton_delete_instruct)

        self.comboBox_select_command = QComboBox()
        self.comboBox_select_command.addItems(list(command_link_dict.keys()))
        self.comboBox_select_command.setSizeAdjustPolicy(QComboBox.AdjustToContents)  # 设置为自适应大小
        self.horizontalLayout.addWidget(self.comboBox_select_command)

        self.widget_command_setting = QWidget()
        self.horizontalLayout_command_setting = QHBoxLayout()
        self.horizontalLayout_command_setting.setSpacing(0)
        self.horizontalLayout_command_setting.setContentsMargins(0, 0, 0, 0)
        self.widget_command_setting.setLayout(self.horizontalLayout_command_setting)
        self.horizontalLayout.addWidget(self.widget_command_setting)

        self.horizontalLayout.setStretch(4, 1)

        """
        槽函数设置
        """
        self.comboBox_select_command.currentTextChanged.connect(self.select_command)

        """
        初始化
        """
        self.args_dict_config = args_dict_config

        if self.args_dict_config:  # 根据传入字典中的项，自动创建对应控件
            current_command = self.args_dict_config['command_type']
            self.args_dict_config = convert_args_dict(self.args_dict_config)  # 转换格式
            self.comboBox_select_command.setCurrentText(current_command)
            self.select_command(current_command)  # 手动执行一次，防止当前项与默认项为同一个而不触发更新信号

    def select_command(self, command: str):
        """选择命令"""
        print(f'传递给子控件的参数 {self.args_dict_config}')
        self.child_widget_command = eval(
            f"{command_link_dict[command]['widget']}(self.args_dict_config)")  # 利用字典获取不同命令对应的控件，并利用eval将字符串转换为对象
        layout = self.widget_command_setting.layout()  # 获取对应控件组中用于存放不同命令控件的控件的布局

        while layout.count():  # 先清空布局中的原有控件
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.child_widget_command:
            layout.addWidget(self.child_widget_command)
            self.child_widget_command.signal_args.connect(self.get_command_signal)
            self.child_widget_command.send_args()  # 执行一次子控件的发送信号函数，用于发送初始数据

    def get_command_signal(self, args_dict):
        """获取子控件的信号，并发送"""
        print(f'子控件传回的参数 {args_dict}')
        self.signal_send_args.emit(args_dict)


class command_widget_move_mouse_to_position(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
		更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_duration = default_args_dict_copy['max_duration']
        default_duration = default_args_dict_copy['default_duration']
        max_x = default_args_dict_copy['max_x']
        default_x = default_args_dict_copy['default_x']
        max_y = default_args_dict_copy['max_y']
        default_y = default_args_dict_copy['default_y']


        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setText('使用')
        self.horizontalLayout.addWidget(self.label)

        self.doubleSpinBox_duration = QDoubleSpinBox()
        self.doubleSpinBox_duration.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_duration.setMaximum(max_duration)
        self.doubleSpinBox_duration.setValue(default_duration)
        self.horizontalLayout.addWidget(self.doubleSpinBox_duration)

        self.label_2 = QLabel()
        self.label_2.setText('秒，移动至 (x:')
        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_x = QSpinBox()
        self.spinBox_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_x.setMaximum(max_x)
        self.spinBox_x.setValue(default_x)
        self.horizontalLayout.addWidget(self.spinBox_x)

        self.label_3 = QLabel()
        self.label_3.setText(',y:')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_y = QSpinBox()
        self.spinBox_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_y.setMaximum(max_y)
        self.spinBox_y.setValue(default_y)
        self.horizontalLayout.addWidget(self.spinBox_y)

        self.label_4 = QLabel()
        self.label_4.setText(')')
        self.horizontalLayout.addWidget(self.label_4)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.spinBox_x.valueChanged.connect(self.check_args)
        self.spinBox_y.valueChanged.connect(self.check_args)

        self.spinBox_x.valueChanged.connect(self.send_args)
        self.spinBox_y.valueChanged.connect(self.send_args)
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        if self.spinBox_x.value() == 0 and self.spinBox_y.value() == 0:
            self.right_args = False
            self.spinBox_x.setStyleSheet(error_stylesheet_border)
            self.spinBox_y.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.spinBox_x.setStyleSheet('')
            self.spinBox_y.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        x = self.spinBox_x.value()
        y = self.spinBox_y.value()
        duration = self.doubleSpinBox_duration.value()

        args_dict = {'right_args': right_args,
                     'x': x,
                     'y': y,
                     'duration': duration}

        self.signal_args.emit(args_dict)


class command_widget_drag_mouse_to_position(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_duration = args_dict_config['max_duration']
        default_duration = args_dict_config['default_duration']
        max_x = args_dict_config['max_x']
        default_x = args_dict_config['default_x']
        max_y = args_dict_config['max_y']
        default_y = args_dict_config['default_y']
        default_button = args_dict_config['default_button']

        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setText('按下')
        self.horizontalLayout.addWidget(self.label)

        self.comboBox_button = QComboBox()
        self.comboBox_button.addItems(['左键', '右键', '中键'])
        self.comboBox_button.setCurrentText(default_button)
        self.horizontalLayout.addWidget(self.comboBox_button)

        self.label_2 = QLabel()
        self.label_2.setText('，并使用')
        self.horizontalLayout.addWidget(self.label_2)

        self.doubleSpinBox_duration = QDoubleSpinBox()
        self.doubleSpinBox_duration.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_duration.setMaximum(max_duration)
        self.doubleSpinBox_duration.setValue(default_duration)
        self.horizontalLayout.addWidget(self.doubleSpinBox_duration)

        self.label_3 = QLabel()
        self.label_3.setText('秒拖拽至 (x:')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_x = QSpinBox()
        self.spinBox_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_x.setMaximum(max_x)
        self.spinBox_x.setValue(default_x)
        self.horizontalLayout.addWidget(self.spinBox_x)

        self.label_4 = QLabel()
        self.label_4.setText(',y:')
        self.horizontalLayout.addWidget(self.label_4)

        self.spinBox_y = QSpinBox()
        self.spinBox_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_y.setMaximum(max_y)
        self.spinBox_y.setValue(default_y)
        self.horizontalLayout.addWidget(self.spinBox_y)

        self.label_5 = QLabel()
        self.label_5.setText(') 释放')
        self.horizontalLayout.addWidget(self.label_5)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.spinBox_x.valueChanged.connect(self.check_args)
        self.spinBox_y.valueChanged.connect(self.check_args)

        self.spinBox_x.valueChanged.connect(self.send_args)
        self.spinBox_y.valueChanged.connect(self.send_args)
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)
        self.comboBox_button.currentTextChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        if self.spinBox_x.value() == 0 and self.spinBox_y.value() == 0:
            self.right_args = False
            self.spinBox_x.setStyleSheet(error_stylesheet_border)
            self.spinBox_y.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.spinBox_x.setStyleSheet('')
            self.spinBox_y.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        x = self.spinBox_x.value()
        y = self.spinBox_y.value()
        duration = self.doubleSpinBox_duration.value()
        button = self.comboBox_button.currentText()

        args_dict = {'right_args': right_args,
                     'x': x,
                     'y': y,
                     'duration': duration,
                     'button': button}

        self.signal_args.emit(args_dict)


class command_widget_mouse_click(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_button = default_args_dict_copy['default_button']
        default_clicks = default_args_dict_copy['default_clicks']
        max_clicks = default_args_dict_copy['max_clicks']
        max_interval = default_args_dict_copy['max_interval']
        default_interval = default_args_dict_copy['default_interval']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_5 = QLabel()
        self.label_5.setText('点击')
        self.horizontalLayout.addWidget(self.label_5)

        self.comboBox_button = QComboBox()
        self.comboBox_button.addItems(['左键', '右键', '中键'])
        self.comboBox_button.setCurrentText(default_button)
        self.horizontalLayout.addWidget(self.comboBox_button)

        self.spinBox_clicks = QSpinBox()
        self.spinBox_clicks.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_clicks.setValue(default_clicks)
        self.spinBox_clicks.setMaximum(max_clicks)
        self.horizontalLayout.addWidget(self.spinBox_clicks)

        self.label_6 = QLabel()
        self.label_6.setText('次，点击间隔时间')
        self.horizontalLayout.addWidget(self.label_6)

        self.doubleSpinBox_interval = QDoubleSpinBox()
        self.doubleSpinBox_interval.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_interval.setMaximum(max_interval)
        self.doubleSpinBox_interval.setValue(default_interval)
        self.horizontalLayout.addWidget(self.doubleSpinBox_interval)

        self.label_7 = QLabel()
        self.label_7.setText('秒')
        self.horizontalLayout.addWidget(self.label_7)

        """
        初始化
        """
        self.right_args = True
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_button.currentTextChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)
        self.spinBox_clicks.valueChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        button = self.comboBox_button.currentText()
        interval = self.doubleSpinBox_interval.value()
        clicks = self.spinBox_clicks.value()

        args_dict = {'right_args': right_args,
                     'button': button,
                     'interval': interval,
                     'clicks': clicks}

        self.signal_args.emit(args_dict)


class command_widget_mouse_down(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_button = default_args_dict_copy['default_button']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_5 = QLabel()
        self.label_5.setText('按下')
        self.horizontalLayout.addWidget(self.label_5)

        self.comboBox_button = QComboBox()
        self.comboBox_button.addItems(['左键', '右键', '中键'])
        self.comboBox_button.setCurrentText(default_button)
        self.horizontalLayout.addWidget(self.comboBox_button)

        self.label_6 = QLabel()
        self.label_6.setText('不释放')
        self.horizontalLayout.addWidget(self.label_6)

        """
        初始化
        """
        self.right_args = True
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_button.currentTextChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        button = self.comboBox_button.currentText()

        args_dict = {'right_args': right_args,
                     'button': button}

        self.signal_args.emit(args_dict)


class command_widget_mouse_up(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_button = default_args_dict_copy['default_button']
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
        self.right_args = True
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_button.currentTextChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        button = self.comboBox_button.currentText()

        args_dict = {'right_args': right_args,
                     'button': button}

        self.signal_args.emit(args_dict)


class command_widget_mouse_scroll(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_direction = default_args_dict_copy['default_direction']
        default_distance = default_args_dict_copy['default_distance']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_4 = QLabel()
        self.label_4.setText('使用滚轮')
        self.horizontalLayout.addWidget(self.label_4)

        self.comboBox_scroll_direction = QComboBox()
        self.comboBox_scroll_direction.addItems(['向上', '向下'])
        self.comboBox_scroll_direction.setCurrentText(default_direction)
        self.horizontalLayout.addWidget(self.comboBox_scroll_direction)

        self.label_5 = QLabel()
        self.label_5.setText('滚动')
        self.horizontalLayout.addWidget(self.label_5)

        self.spinBox_scroll_distance = QSpinBox()
        self.spinBox_scroll_distance.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_scroll_distance.setMaximum(9999)
        self.spinBox_scroll_distance.setValue(default_distance)
        self.horizontalLayout.addWidget(self.spinBox_scroll_distance)

        self.label_6 = QLabel()
        self.label_6.setText('像素距离')
        self.horizontalLayout.addWidget(self.label_6)

        """
        初始化
        """
        self.right_args = True
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_scroll_direction.currentTextChanged.connect(self.send_args)
        self.spinBox_scroll_distance.valueChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        distance = + self.spinBox_scroll_distance.value() if self.comboBox_scroll_direction.currentText() == '向上' \
            else - self.spinBox_scroll_distance.value()

        args_dict = {'right_args': right_args,
                     'distance': distance}

        self.signal_args.emit(args_dict)


class command_widget_press_text(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_interval = default_args_dict_copy['max_interval']
        default_interval = default_args_dict_copy['default_interval']
        default_message = default_args_dict_copy['default_message']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('逐词输入')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_message = QLineEdit()
        self.lineEdit_message.setPlaceholderText('输入文本')
        if default_message:
            self.lineEdit_message.setText(default_message)
        self.horizontalLayout.addWidget(self.lineEdit_message)

        self.label_3 = QLabel()
        self.label_3.setText('文本，输入间隔')
        self.horizontalLayout.addWidget(self.label_3)

        self.doubleSpinBox_interval = QDoubleSpinBox()
        self.doubleSpinBox_interval.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_interval.setMaximum(max_interval)
        self.doubleSpinBox_interval.setValue(default_interval)
        self.horizontalLayout.addWidget(self.doubleSpinBox_interval)

        self.label_4 = QLabel()
        self.label_4.setText('秒')
        self.horizontalLayout.addWidget(self.label_4)

        """
        初始化
        """
        self.right_args = True
        self.send_args()

        """"
        槽函数设置
        """
        self.lineEdit_message.textChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        message = self.lineEdit_message.text()
        interval = self.doubleSpinBox_interval.value()

        args_dict = {'right_args': right_args,
                     'message': message,
                     'interval': interval}

        self.signal_args.emit(args_dict)


class command_widget_press_keys(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_interval = default_args_dict_copy['max_interval']
        default_interval = default_args_dict_copy['default_interval']
        default_keys = default_args_dict_copy['default_keys']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('逐个输入')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_keys = QLineEdit()
        self.lineEdit_keys.setPlaceholderText('指定名称的键，以空格间隔')
        if default_keys:
            self.lineEdit_keys.setText(default_keys)
        self.horizontalLayout.addWidget(self.lineEdit_keys)

        self.label_3 = QLabel()
        self.label_3.setText('中的键，重复')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_presses = QSpinBox()
        self.spinBox_presses.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.horizontalLayout.addWidget(self.spinBox_presses)

        self.label_4 = QLabel()
        self.label_4.setText('次，每次重复间隔')
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
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_keys.textChanged.connect(self.check_args)

        self.lineEdit_keys.textChanged.connect(self.send_args)
        self.spinBox_presses.valueChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        keys_split = self.lineEdit_keys.text().split(" ")
        wrong_key = [key for key in keys_split if key.lower() not in pyautogui_keyboard_keys and key.strip()]
        if wrong_key:
            self.right_args = False
            self.lineEdit_keys.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.lineEdit_keys.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        keys_split = self.lineEdit_keys.text().split(" ")
        keys = [key for key in keys_split if key.lower() in pyautogui_keyboard_keys]
        keys = keys if keys else ''  # keys不能设置为[]

        presses = self.spinBox_presses.value()
        interval = self.doubleSpinBox_interval.value()

        args_dict = {'right_args': right_args,
                     'keys': keys,
                     'presses': presses,
                     'interval': interval}

        self.signal_args.emit(args_dict)


class command_widget_press_hotkey(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_hotkeys = default_args_dict_copy['default_hotkeys']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('使用')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_hotkeys = QLineEdit()
        self.lineEdit_hotkeys.setPlaceholderText('指定名称的键，以空格间隔')
        if default_hotkeys:
            self.lineEdit_hotkeys.setText(default_hotkeys)
        self.horizontalLayout.addWidget(self.lineEdit_hotkeys)

        self.label_3 = QLabel()
        self.label_3.setText('热键')
        self.horizontalLayout.addWidget(self.label_3)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_hotkeys.textChanged.connect(self.check_args)

        self.lineEdit_hotkeys.textChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        keys_split = self.lineEdit_hotkeys.text().split(" ")
        wrong_key = [key for key in keys_split if key.lower() not in pyautogui_keyboard_keys and key.strip()]
        if wrong_key:
            self.right_args = False
            self.lineEdit_hotkeys.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.lineEdit_hotkeys.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        keys_split = self.lineEdit_hotkeys.text().split(" ")
        hotkeys = [key for key in keys_split if key.lower() in pyautogui_keyboard_keys]
        hotkeys = hotkeys if hotkeys else ''  # hotkeys不能设置为[]

        args_dict = {'right_args': right_args,
                     'hotkeys': hotkeys}

        self.signal_args.emit(args_dict)


class command_widget_press_down_key(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_key = default_args_dict_copy['default_key']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('按下')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_key = QLineEdit()
        self.lineEdit_key.setPlaceholderText('仅支持单键，指定名称的键')
        if default_key:
            self.lineEdit_key.setText(default_key)
        self.horizontalLayout.addWidget(self.lineEdit_key)

        self.label_3 = QLabel()
        self.label_3.setText('键（不释放，但不会重复输入文本）')
        self.horizontalLayout.addWidget(self.label_3)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_key.textChanged.connect(self.check_args)

        self.lineEdit_key.textChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        key = self.lineEdit_key.text().strip()
        if key.lower() not in pyautogui_keyboard_keys:
            self.right_args = False
            self.lineEdit_key.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.lineEdit_key.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        key = self.lineEdit_key.text().strip()

        args_dict = {'right_args': right_args,
                     'key': key}

        self.signal_args.emit(args_dict)


class command_widget_press_up_key(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_key = default_args_dict_copy['default_key']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('释放')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_key = QLineEdit()
        self.lineEdit_key.setPlaceholderText('仅支持单键，指定名称的键')
        if default_key:
            self.lineEdit_key.setText(default_key)
        self.horizontalLayout.addWidget(self.lineEdit_key)

        self.label_3 = QLabel()
        self.label_3.setText('键')
        self.horizontalLayout.addWidget(self.label_3)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_key.textChanged.connect(self.check_args)

        self.lineEdit_key.textChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        key = self.lineEdit_key.text().strip()
        if key.lower() not in pyautogui_keyboard_keys:
            self.right_args = False
            self.lineEdit_key.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.lineEdit_key.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        key = self.lineEdit_key.text().strip()

        args_dict = {'right_args': right_args,
                     'key': key}

        self.signal_args.emit(args_dict)


class command_widget_screenshot_fullscreen(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_pic_file = default_args_dict_copy['default_pic_file']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('全屏截图，并保存图片至')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_pic_file = QLineEdit()
        self.lineEdit_pic_file.setPlaceholderText('输入文件名（不含后缀），如存在则覆盖')
        if default_pic_file:
            self.lineEdit_pic_file.setText(default_pic_file)
        self.horizontalLayout.addWidget(self.lineEdit_pic_file)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_pic_file.textChanged.connect(self.check_args)

        self.lineEdit_pic_file.textChanged.connect(self.send_args)

    def check_args(self):
        """检查参数规范"""
        pic_file = self.lineEdit_pic_file.text().strip()
        if not pic_file or not check_filename_feasible(pic_file):
            self.right_args = False
            self.lineEdit_pic_file.setStyleSheet(error_stylesheet_border)
        else:

            self.right_args = True
            self.lineEdit_pic_file.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        pic_file_name = self.lineEdit_pic_file.text().strip()
        if pic_file_name:
            pic_file_suffix = '.png'
        else:
            pic_file_suffix = ''
        pic_file = pic_file_name + pic_file_suffix

        args_dict = {'right_args': right_args,
                     'pic_file': pic_file}

        self.signal_args.emit(args_dict)


class command_widget_screenshot_area(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_x = default_args_dict_copy['max_x']
        max_y = default_args_dict_copy['max_y']
        default_area = default_args_dict_copy['default_area']
        default_pic_file = default_args_dict_copy['default_pic_file']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('对 (x1:')
        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_xl = QSpinBox()
        self.spinBox_xl.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_xl.setMaximum(max_x)
        self.spinBox_xl.setValue(default_area[0])
        self.horizontalLayout.addWidget(self.spinBox_xl)

        self.label_3 = QLabel()
        self.label_3.setText(',y1:')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_yl = QSpinBox()
        self.spinBox_yl.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_yl.setMaximum(max_y)
        self.spinBox_yl.setValue(default_area[1])
        self.horizontalLayout.addWidget(self.spinBox_yl)

        self.label_4 = QLabel()
        self.label_4.setText(',x2:')
        self.horizontalLayout.addWidget(self.label_4)

        self.spinBox_xr = QSpinBox()
        self.spinBox_xr.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_xr.setMaximum(max_x)
        self.spinBox_xr.setValue(default_area[2])
        self.horizontalLayout.addWidget(self.spinBox_xr)

        self.label_5 = QLabel()
        self.label_5.setText(',y2:')
        self.horizontalLayout.addWidget(self.label_5)

        self.spinBox_yr = QSpinBox()
        self.spinBox_yr.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_yr.setMaximum(max_y)
        self.spinBox_yr.setValue(default_area[3])
        self.horizontalLayout.addWidget(self.spinBox_yr)

        self.label_6 = QLabel()
        self.label_6.setText(') 区域截图，并保存图片至')
        self.horizontalLayout.addWidget(self.label_6)

        self.lineEdit_pic_file = QLineEdit()
        self.lineEdit_pic_file.setPlaceholderText('输入文件名（不含后缀），如存在则覆盖')
        if default_pic_file:
            self.lineEdit_pic_file.setText(default_pic_file)
        self.horizontalLayout.addWidget(self.lineEdit_pic_file)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.horizontalLayout.addWidget(self.line)

        self.toolButton_locate = QToolButton()
        self.toolButton_locate.setText('定位')
        self.horizontalLayout.addWidget(self.toolButton_locate)

        """
        初始化
        """
        self.right_args_filename = False
        self.right_args_xy = False
        self.check_args_filename()
        self.check_args_xy()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_pic_file.textChanged.connect(self.check_args_filename)
        self.spinBox_xl.valueChanged.connect(self.check_args_xy)
        self.spinBox_yl.valueChanged.connect(self.check_args_xy)
        self.spinBox_xr.valueChanged.connect(self.check_args_xy)
        self.spinBox_yr.valueChanged.connect(self.check_args_xy)

        self.lineEdit_pic_file.textChanged.connect(self.send_args)
        self.spinBox_xl.valueChanged.connect(self.send_args)
        self.spinBox_yl.valueChanged.connect(self.send_args)
        self.spinBox_xr.valueChanged.connect(self.send_args)
        self.spinBox_yr.valueChanged.connect(self.send_args)

        self.toolButton_locate.clicked.connect(self.screenshot)

    def screenshot(self):
        """截屏"""
        dialog = qdialog_screenshot.QDialogScreenshot()
        dialog.signal_screenshot_area.connect(dialog.close)  # 先关闭dialog再进行截图，防止将遮罩也截入
        dialog.signal_screenshot_area.connect(self.get_screenshot_area)
        dialog.exec_()

    def get_screenshot_area(self, screenshot_area: list):
        """获取截屏区域的信号"""
        x_start, y_start, x_end, y_end = screenshot_area
        self.spinBox_xl.setValue(x_start)
        self.spinBox_yl.setValue(y_start)
        self.spinBox_xr.setValue(x_end)
        self.spinBox_yr.setValue(y_end)

    def check_args_filename(self):
        """检查参数规范"""
        pic_file = self.lineEdit_pic_file.text().strip()
        if not pic_file or not check_filename_feasible(pic_file):
            self.right_args_filename = False
            self.lineEdit_pic_file.setStyleSheet(error_stylesheet_border)
        else:

            self.right_args_filename = True
            self.lineEdit_pic_file.setStyleSheet('')

    def check_args_xy(self):
        """检查参数规范"""
        x_1 = self.spinBox_xl.value()
        y_1 = self.spinBox_yl.value()
        x_2 = self.spinBox_xr.value()
        y_2 = self.spinBox_yr.value()

        if x_1 == x_2:
            check_x = False
            self.spinBox_xl.setStyleSheet(error_stylesheet_border)
            self.spinBox_xr.setStyleSheet(error_stylesheet_border)
        else:
            check_x = True
            self.spinBox_xl.setStyleSheet('')
            self.spinBox_xr.setStyleSheet('')

        if y_1 == y_2:
            check_y = False
            self.spinBox_yl.setStyleSheet(error_stylesheet_border)
            self.spinBox_yr.setStyleSheet(error_stylesheet_border)
        else:
            check_y = True
            self.spinBox_yl.setStyleSheet('')
            self.spinBox_yr.setStyleSheet('')

        if check_x and check_y:
            self.right_args_xy = True
        else:
            self.right_args_xy = False

    def send_args(self):
        """发送参数设置"""
        if self.right_args_filename and self.right_args_xy:
            right_args = True
        else:
            right_args = False

        pic_file_name = self.lineEdit_pic_file.text().strip()
        if pic_file_name:
            pic_file_suffix = '.png'
        else:
            pic_file_suffix = ''
        pic_file = pic_file_name + pic_file_suffix

        x_1 = self.spinBox_xl.value()
        y_1 = self.spinBox_yl.value()
        x_2 = self.spinBox_xr.value()
        y_2 = self.spinBox_yr.value()
        xl, xr = sorted([x_1, x_2])
        yl, yr = sorted([y_1, y_2])
        area = (xl, yl, xr, yr)

        args_dict = {'right_args': right_args,
                     'pic_file': pic_file,
                     'area': area}

        self.signal_args.emit(args_dict)


class command_widget_move_to_pic_position(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_duration = default_args_dict_copy['max_duration']
        default_duration = default_args_dict_copy['default_duration']
        default_pic_file = default_args_dict_copy['default_pic_file']
        default_find_model = default_args_dict_copy['default_find_model']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setText('匹配图片')
        self.horizontalLayout.addWidget(self.label)

        self.label_show_pic = DropLabel()
        self.label_show_pic.setText('拖入图片')
        self.label_show_pic.setFrameShape(QFrame.Box)
        self.label_show_pic.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.label_show_pic)

        self.label_2 = QLabel()
        self.label_2.setText('，分别使用')
        self.horizontalLayout.addWidget(self.label_2)

        self.doubleSpinBox_duration = QDoubleSpinBox()
        self.doubleSpinBox_duration.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_duration.setMaximum(max_duration)
        self.doubleSpinBox_duration.setValue(default_duration)
        self.horizontalLayout.addWidget(self.doubleSpinBox_duration)

        self.label_3 = QLabel()
        self.label_3.setText('秒移动鼠标至')
        self.horizontalLayout.addWidget(self.label_3)

        self.comboBox_find_model = QComboBox()
        self.comboBox_find_model.addItems(['第一个', '全部'])
        self.comboBox_find_model.setCurrentText(default_find_model)
        self.horizontalLayout.addWidget(self.comboBox_find_model)

        self.label_4 = QLabel()
        self.label_4.setText('匹配位置')
        self.horizontalLayout.addWidget(self.label_4)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.horizontalLayout.addWidget(self.line)

        self.toolButton_choose_pic = QToolButton()
        self.toolButton_choose_pic.setText('选图')
        self.horizontalLayout.addWidget(self.toolButton_choose_pic)

        self.toolButton_screenshot = QToolButton()
        self.toolButton_screenshot.setText('截图')
        self.horizontalLayout.addWidget(self.toolButton_screenshot)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        if default_pic_file:
            self.choose_pic(default_pic_file)

        """
        槽函数设置
        """
        self.toolButton_choose_pic.clicked.connect(self.choose_pic)
        self.toolButton_screenshot.clicked.connect(self.screenshot)

        self.label_show_pic.signal_QLabel_dropped.connect(self.check_args)

        self.label_show_pic.signal_QLabel_dropped.connect(self.send_args)
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)
        self.comboBox_find_model.currentTextChanged.connect(self.send_args)

    def choose_pic(self, pic_file=None):
        """弹出文件对话框选择图片，并设置label属性
        可传入pic_file参数来跳过对话框"""
        if not pic_file:
            pic_file, _ = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片文件(*.png *.jpg *.bmp)")

        if pic_file:
            self.label_show_pic.setProperty('pic_path', pic_file)
            pixmap = QPixmap(pic_file)
            resize = calculate_resize(self.label_show_pic.size(), pixmap.size())
            pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
            self.label_show_pic.setPixmap(pixmap)

            self.check_args()
            self.send_args()

    def screenshot(self):
        """截屏"""
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

        format_area = (x_start, y_start, x_end - x_start, y_end - y_start)

        pic_name = f'screenshot_{create_random_string(8)}.png'
        save_pic_file = os.path.normpath(os.path.join(os.getcwd(), 'screenshot', pic_name))
        print(f'截图存放路径 {save_pic_file}')
        pyautogui.screenshot(save_pic_file, region=format_area)
        self.choose_pic(save_pic_file)

        self.check_args()

    def check_args(self):
        """检查参数规范"""
        pic_file = self.label_show_pic.property('pic_path')
        if not pic_file or not os.path.exists(pic_file) or not filetype.is_image(pic_file):
            self.right_args = False
            self.label_show_pic.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.label_show_pic.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        pic_file_property = self.label_show_pic.property('pic_path')
        pic_file = pic_file_property if pic_file_property else ''  # pic_file不能是None

        find_model = self.comboBox_find_model.currentText()
        duration = self.doubleSpinBox_duration.value()

        args_dict = {'right_args': right_args,
                     'pic_file': pic_file,
                     'duration': duration,
                     'find_model': find_model}

        self.signal_args.emit(args_dict)


class command_widget_click_pic_position(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        max_duration = default_args_dict_copy['max_duration']
        default_duration = default_args_dict_copy['default_duration']
        default_button = default_args_dict_copy['default_button']
        default_clicks = default_args_dict_copy['default_clicks']
        max_clicks = default_args_dict_copy['max_clicks']
        max_interval = default_args_dict_copy['max_interval']
        default_interval = default_args_dict_copy['default_interval']
        default_pic_file = default_args_dict_copy['default_pic_file']
        default_find_model = default_args_dict_copy['default_find_model']
        """
        ui设置
        """
        self.horizontalLayout_top = QHBoxLayout(self)
        self.horizontalLayout_top.setSpacing(5)
        self.horizontalLayout_top.setContentsMargins(0, 0, 0, 0)

        # 第1列布局
        self.horizontalLayout_line1 = QHBoxLayout()

        self.label = QLabel()
        self.label.setText('匹配图片')
        self.horizontalLayout_line1.addWidget(self.label)

        self.label_show_pic = DropLabel()
        self.label_show_pic.setText('拖入图片')
        self.label_show_pic.setFrameShape(QFrame.Box)
        self.label_show_pic.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_line1.addWidget(self.label_show_pic)

        self.label_2 = QLabel()
        self.label_2.setText('，分别使用')
        self.horizontalLayout_line1.addWidget(self.label_2)

        self.doubleSpinBox_duration = QDoubleSpinBox()
        self.doubleSpinBox_duration.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_duration.setMaximum(max_duration)
        self.doubleSpinBox_duration.setValue(default_duration)
        self.horizontalLayout_line1.addWidget(self.doubleSpinBox_duration)

        self.label_3 = QLabel()
        self.label_3.setText('秒移动鼠标至')
        self.horizontalLayout_line1.addWidget(self.label_3)

        self.comboBox_find_model = QComboBox()
        self.comboBox_find_model.addItems(['第一个', '全部'])
        self.comboBox_find_model.setCurrentText(default_find_model)
        self.horizontalLayout_line1.addWidget(self.comboBox_find_model)

        self.label_4 = QLabel()
        self.label_4.setText('匹配位置，')
        self.horizontalLayout_line1.addWidget(self.label_4)

        # 第2列布局
        self.horizontalLayout_line2 = QHBoxLayout()

        self.label_5 = QLabel()
        self.label_5.setText('并点击')
        self.horizontalLayout_line2.addWidget(self.label_5)

        self.comboBox_button = QComboBox()
        self.comboBox_button.addItems(['左键', '右键', '中键'])
        self.comboBox_button.setCurrentText(default_button)
        self.horizontalLayout_line2.addWidget(self.comboBox_button)

        self.spinBox_clicks = QSpinBox()
        self.spinBox_clicks.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_clicks.setValue(default_clicks)
        self.spinBox_clicks.setMinimum(1)
        self.spinBox_clicks.setMaximum(max_clicks)
        self.horizontalLayout_line2.addWidget(self.spinBox_clicks)

        self.label_6 = QLabel()
        self.label_6.setText('次，点击间隔时间')
        self.horizontalLayout_line2.addWidget(self.label_6)

        self.doubleSpinBox_interval = QDoubleSpinBox()
        self.doubleSpinBox_interval.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_interval.setMaximum(max_interval)
        self.doubleSpinBox_interval.setValue(default_interval)
        self.horizontalLayout_line2.addWidget(self.doubleSpinBox_interval)

        self.label_7 = QLabel()
        self.label_7.setText('秒')
        self.horizontalLayout_line2.addWidget(self.label_7)

        # 右侧按钮布局
        self.horizontalLayout_button = QHBoxLayout()

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_button.addWidget(self.line)

        self.toolButton_choose_pic = QToolButton()
        self.toolButton_choose_pic.setText('选图')
        self.horizontalLayout_button.addWidget(self.toolButton_choose_pic)

        self.toolButton_screenshot = QToolButton()
        self.toolButton_screenshot.setText('截图')
        self.horizontalLayout_button.addWidget(self.toolButton_screenshot)

        # 合并两列布局
        self.verticalLayout_line = QVBoxLayout()
        self.verticalLayout_line.addLayout(self.horizontalLayout_line1)
        self.verticalLayout_line.addLayout(self.horizontalLayout_line2)

        # 组合全部布局
        self.horizontalLayout_top.addLayout(self.verticalLayout_line)
        self.horizontalLayout_top.addLayout(self.horizontalLayout_button)

        """
        初始化
        """
        self.right_args = False
        self.check_args()
        self.send_args()

        if default_pic_file:
            self.choose_pic(default_pic_file)

        """
        槽函数设置
        """
        self.toolButton_choose_pic.clicked.connect(self.choose_pic)
        self.toolButton_screenshot.clicked.connect(self.screenshot)

        self.label_show_pic.signal_QLabel_dropped.connect(self.check_args)

        self.label_show_pic.signal_QLabel_dropped.connect(self.send_args)
        self.doubleSpinBox_duration.valueChanged.connect(self.send_args)
        self.comboBox_find_model.currentTextChanged.connect(self.send_args)
        self.comboBox_button.currentTextChanged.connect(self.send_args)
        self.spinBox_clicks.valueChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)

    def choose_pic(self, pic_file=None):
        """弹出文件对话框选择图片，并设置label属性
        可传入pic_file参数来跳过对话框"""
        if not pic_file:
            pic_file, _ = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片文件(*.png *.jpg *.bmp)")

        if pic_file:
            self.label_show_pic.setProperty('pic_path', pic_file)
            pixmap = QPixmap(pic_file)
            resize = calculate_resize(self.label_show_pic.size(), pixmap.size())
            pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
            self.label_show_pic.setPixmap(pixmap)

            self.check_args()
            self.send_args()

    def screenshot(self):
        """截屏"""
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

        format_area = (x_start, y_start, x_end - x_start, y_end - y_start)
        pic_name = f'screenshot_{create_random_string(8)}.png'
        save_pic_file = os.path.normpath(os.path.join(os.getcwd(),'screenshot',pic_name))
        print(f'截图存放路径 {save_pic_file}')
        pyautogui.screenshot(save_pic_file, region=format_area)
        self.choose_pic(save_pic_file)

        self.check_args()

    def check_args(self):
        """检查参数规范"""
        pic_file = self.label_show_pic.property('pic_path')
        if not pic_file or not os.path.exists(pic_file) or not filetype.is_image(pic_file):
            self.right_args = False
            self.label_show_pic.setStyleSheet(error_stylesheet_border)
        else:
            self.right_args = True
            self.label_show_pic.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        pic_file_property = self.label_show_pic.property('pic_path')
        pic_file = pic_file_property if pic_file_property else ''  # pic_file不能是None

        find_model = self.comboBox_find_model.currentText()
        duration = self.doubleSpinBox_duration.value()
        button = self.comboBox_button.currentText()
        clicks = self.spinBox_clicks.value()
        interval = self.doubleSpinBox_interval.value()

        args_dict = {'right_args': right_args,
                     'pic_file': pic_file,
                     'duration': duration,
                     'find_model': find_model,
                     'button': button,
                     'clicks': clicks,
                     'interval': interval}

        self.signal_args.emit(args_dict)


class command_widget_wait(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_wait_time = default_args_dict_copy['default_wait_time']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('等待')
        self.horizontalLayout.addWidget(self.label_2)

        self.doubleSpinBox_wait_time = QDoubleSpinBox()
        self.doubleSpinBox_wait_time.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_wait_time.setMaximum(9999.99)
        self.doubleSpinBox_wait_time.setValue(default_wait_time)
        self.horizontalLayout.addWidget(self.doubleSpinBox_wait_time)

        self.label_3 = QLabel()
        self.label_3.setText('秒')
        self.horizontalLayout.addWidget(self.label_3)

        """
        初始化
        """
        self.right_args = True
        self.send_args()

        """
        槽函数设置
        """
        self.doubleSpinBox_wait_time.valueChanged.connect(self.send_args)

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args
        wait_time = self.doubleSpinBox_wait_time.value()

        args_dict = {'right_args': right_args,
                     'wait_time': wait_time}

        self.signal_args.emit(args_dict)


class command_widget_wait_random(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key in args_dict_config:
                value = args_dict_config[key]
                default_args_dict_copy[key] = value
        default_wait_time_min = default_args_dict_copy['default_wait_time_min']
        default_wait_time_max = default_args_dict_copy['default_wait_time_max']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setText('等待（区间内随机数） 最小值')
        self.horizontalLayout.addWidget(self.label)

        self.doubleSpinBox_wait_time_min = QDoubleSpinBox()
        self.doubleSpinBox_wait_time_min.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_wait_time_min.setMaximum(9999.99)
        self.doubleSpinBox_wait_time_min.setValue(default_wait_time_min)
        self.horizontalLayout.addWidget(self.doubleSpinBox_wait_time_min)

        self.label_2 = QLabel()
        self.label_2.setText('秒~最大值')
        self.horizontalLayout.addWidget(self.label_2)

        self.doubleSpinBox_wait_time_max = QDoubleSpinBox()
        self.doubleSpinBox_wait_time_max.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_wait_time_max.setMaximum(9999.99)
        self.doubleSpinBox_wait_time_max.setValue(default_wait_time_max)
        self.horizontalLayout.addWidget(self.doubleSpinBox_wait_time_max)

        self.label_3 = QLabel()
        self.label_3.setText('秒')
        self.horizontalLayout.addWidget(self.label_3)

        """
        初始化
        """
        self.right_args = True
        self.send_args()

        """
        槽函数设置
        """
        self.doubleSpinBox_wait_time_min.valueChanged.connect(self.send_args)
        self.doubleSpinBox_wait_time_max.valueChanged.connect(self.send_args)

    def send_args(self):
        """发送参数设置"""
        right_args = self.right_args

        wait_time_min = self.doubleSpinBox_wait_time_min.value()
        wait_time_max = self.doubleSpinBox_wait_time_max.value()
        wait_time = (wait_time_min, wait_time_max)

        args_dict = {'right_args': right_args,
                     'wait_time': wait_time}

        self.signal_args.emit(args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = command_widget_mouse_click()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
