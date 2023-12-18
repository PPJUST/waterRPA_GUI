"""命令控件组，命令行相关操作在该模块实现"""

from PySide6.QtCore import *
from PySide6.QtGui import *

from module.function_convert_command import *


class WidgetCommandControl(QWidget):
    """整行指令控件组，作为内部指令行的容器"""
    signal_send_args = Signal(dict)  # 子控件信号的中转发送

    def __init__(self):
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

        self.toolButton_add_command = QToolButton()
        self.toolButton_add_command.setIcon(QIcon(icon_add))
        self.horizontalLayout.addWidget(self.toolButton_add_command)

        self.toolButton_copy_command = QToolButton()
        self.toolButton_copy_command.setIcon(QIcon(icon_copy))
        self.horizontalLayout.addWidget(self.toolButton_copy_command)

        self.toolButton_delete_command = QToolButton()
        self.toolButton_delete_command.setIcon(QIcon(icon_del))
        self.horizontalLayout.addWidget(self.toolButton_delete_command)

        self.comboBox_select_command = QComboBox()
        self.comboBox_select_command.addItems(list(command_chs_to_en_dict.keys()))
        self.comboBox_select_command.setSizeAdjustPolicy(QComboBox.AdjustToContents)  # 设置为自适应大小
        setattr(self.comboBox_select_command, "wheelEvent", lambda a: None)  # 禁用滚轮事件
        self.horizontalLayout.addWidget(self.comboBox_select_command)

        self.widget_command_setting = QWidget()
        self.horizontalLayout_command_setting = QHBoxLayout()
        self.horizontalLayout_command_setting.setSpacing(0)
        self.horizontalLayout_command_setting.setContentsMargins(0, 0, 0, 0)
        self.widget_command_setting.setLayout(self.horizontalLayout_command_setting)
        self.horizontalLayout.addWidget(self.widget_command_setting)

        self.horizontalLayout.setStretch(5, 1)

        """
        连接信号
        """
        self.comboBox_select_command.currentTextChanged.connect(self.select_command)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()

    def load_command_args(self, args_dict):
        """加载命令参数"""
        command_type = self.args_dict['command_type']

        if args_dict:
            self.args_dict = args_dict
            command_type = args_dict['command_type']
            if command_type in command_en_to_chs_dict:  # 转换为中文项
                command_type = command_en_to_chs_dict[command_type]
            self.comboBox_select_command.setCurrentText(command_type)
        self.select_command(command_type)  # 手动执行一次，防止当前项与默认项为同一个而不触发更新信号

    def select_command(self, command_type_chs: str):
        """选择命令"""
        # 先清空
        layout = self.widget_command_setting.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 再添加
        convert = CommandConvert(command_type_chs)
        command_widget_object = convert.get_widget_object()
        command_type_en = convert.get_command_type()
        self.args_dict['command_type'] = command_type_en  # 写入指令名
        if command_widget_object:
            command_widget = command_widget_object()
            command_widget.load_args(self.args_dict)
            layout.addWidget(command_widget)
            command_widget.signal_args.connect(self.get_command_signal)
            command_widget.send_args()  # 执行一次子控件的发送信号函数，用于发送初始数据

    def get_command_signal(self, args_dict):
        """获取子控件的信号，并发送"""
        self.signal_send_args.emit(args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = WidgetCommandControl()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
