import time

from PySide6.QtCore import *

from module import function_config


class ThreadRunCommands(QThread):
    signal_succeed = Signal(str)  # 发送执行成功的控件组id
    signal_failed = Signal(str)  # 发送执行失败的控件组id
    signal_finished = Signal(bool)  # 执行完成后，发送带结束状态的信号
    signal_error = Signal(str)  # 执行报错，发送错误信息

    def __init__(self, parent=None):
        super().__init__(parent)
        self.command_function_dict = {}
        self.find_image_timeout = function_config.get_config_find_image_timeout()
        self.wait_time = function_config.get_config_wait_time()

    def set_command_function(self, command_function):
        """设置参数"""
        self.command_function_dict.clear()
        self.command_function_dict = command_function

    def run(self):
        result_code = True  # 结果正确性，如果错误则False
        for item_id, function in self.command_function_dict.items():
            try:
                if function:
                    result = function()
                    if result:
                        self.signal_succeed.emit(item_id)
                    else:
                        self.signal_failed.emit(item_id)
                        result_code = False
                        break
            except Exception as e:
                # 备忘录 - 报错后释放已经按下的键
                self.signal_failed.emit(item_id)
                error_message = f'运行出错：{e}'
                self.signal_error.emit(error_message)
                result_code = False
                break

            if self.wait_time:
                time.sleep(self.wait_time)

        self.signal_finished.emit(result_code)
