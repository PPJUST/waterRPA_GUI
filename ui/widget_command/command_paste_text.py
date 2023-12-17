from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandPasteText(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('粘贴')
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_message = QLineEdit()
        self.lineEdit_message.setPlaceholderText('键入文本')
        if default_message:
            self.lineEdit_message.setText(default_message)
        self.horizontalLayout.addWidget(self.lineEdit_message)

        self.label_3 = QLabel()
        self.label_3.setText('文本，执行')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_presses = QSpinBox()
        self.spinBox_presses.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_presses.setValue(default_presses)
        self.horizontalLayout.addWidget(self.spinBox_presses)

        self.label_4 = QLabel()
        self.label_4.setText('次，每次执行间隔')
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
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """"
        槽函数设置
        """
        self.lineEdit_message.textChanged.connect(self.send_args)
        self.spinBox_presses.valueChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        interval = args_dict['interval']
        message = args_dict['message']
        presses = args_dict['presses']
        self.doubleSpinBox_interval.setValue(interval)
        self.lineEdit_message.setText(message)
        self.spinBox_presses.setValue(presses)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        message = self.lineEdit_message.text()
        presses = self.spinBox_presses.value()
        interval = self.doubleSpinBox_interval.value()
        self.args_dict['message'] = message
        self.args_dict['presses'] = presses
        self.args_dict['interval'] = interval

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandPasteText()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
