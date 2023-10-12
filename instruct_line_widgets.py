"""
单个控件组内部的操作都在该模块实现
"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

"""
定义常量
"""
code_command_dict = {'': '',
                     '单击左键':'widget_command_pic',
                     '双击左键':'widget_command_pic',
                     '单击右键':'widget_command_pic',
                     '输入文本':'widget_command_input',
                     '等待':'widget_command_wait',
                     '滚动滚轮':'widget_command_scroll',
                     '热键':'widget_command_hotkey',
                     '自定义命令':'widget_command_custom'}  # 第一个元素留空，用于初始显示


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


    def select_command(self, command:str):
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

        self.label_show_pic = QLabel()
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

    def choose_pic(self):
        """弹出文件对话框选择图片"""

        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片文件(*.png *.jpg *.bmp)")
        if file_name:
            self.label_show_pic.setPixmap(QPixmap(file_name))  # 备忘录 后期改为自适应大小


    def screenshot(self):
        """截屏"""
        # 备忘录 需要实现一个置顶遮罩效果，然后将截取的区域使用相关库进行截图操作

    # 备忘录 图片label需要支持拖入操作





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
    """热键指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_7 = QHBoxLayout(self)

        self.lineEdit_hotkey = QLineEdit(self)
        self.lineEdit_hotkey.setObjectName(u"lineEdit_hotkey")
        self.lineEdit_hotkey.setPlaceholderText("多个热键用空格或逗号隔开，效果为同时按下")
        self.horizontalLayout_7.addWidget(self.lineEdit_hotkey)


class widget_command_custom(QWidget):
    """自定义指令设置"""

    def __init__(self):
        super().__init__()
        self.horizontalLayout_8 = QHBoxLayout(self)

        self.comboBox_custom_command = QComboBox()
        self.comboBox_custom_command.setObjectName(u"comboBox_custom_command")
        self.horizontalLayout_8.addWidget(self.comboBox_custom_command)


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
