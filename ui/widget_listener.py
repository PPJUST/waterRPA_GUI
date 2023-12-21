"""自定义dialog控件"""
import time

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.function_convert_listener import convert_to_pyautogui
from module.function_pynput import ListenerPynput


class DialogListener(QDialog):
    signal_send_listener = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        """ui设置"""
        self.layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setText('开始录制，按ESC结束录制(结束后写入数据时会卡顿一段时间)')
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # 设置无边框

        """子线程设置"""
        self.thread = ThreadListener()
        self.thread.signal_finished.connect(self.get_signal)
        self.thread.start()

    def get_signal(self, command_listener):
        self.label.setText('完成录制，等待程序写入配置文件')
        self.signal_send_listener.emit(command_listener)
        self.reject()


class ThreadListener(QThread):
    signal_finished = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener_mouse, self.listener_keyboard = ListenerPynput().get_listener()

    def run(self):
        self.listener_mouse.start()
        self.listener_keyboard.start()
        self.listener_keyboard.join()
        self.listener_keyboard.wait()

        self.listener_keyboard.stop()
        self.listener_mouse.stop()
        command_listener = convert_to_pyautogui()
        self.signal_finished.emit(command_listener)
