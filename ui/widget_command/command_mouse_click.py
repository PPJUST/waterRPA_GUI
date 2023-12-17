from PySide6.QtCore import *
from PySide6.QtWidgets import *

from module.constant_default import *


class CommandMouseClick(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
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
        self.args_dict = default_args_dict.copy()
        self.check_args()
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_button.currentTextChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)
        self.spinBox_clicks.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        button = args_dict['button']
        clicks = args_dict['clicks']
        interval = args_dict['interval']

        self.comboBox_button.setCurrentText(button)
        self.spinBox_clicks.setValue(clicks)
        self.doubleSpinBox_interval.setValue(interval)

    def check_args(self):
        """检查参数规范"""
        pass

    def send_args(self):
        """发送参数设置"""
        button = self.comboBox_button.currentText()
        interval = self.doubleSpinBox_interval.value()
        clicks = self.spinBox_clicks.value()
        self.args_dict['button'] = button
        self.args_dict['interval'] = interval
        self.args_dict['clicks'] = clicks

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMouseClick()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec()


if __name__ == "__main__":
    _test_widget()
