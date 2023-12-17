from ui.widget_command.command_move_to_pic_position import *


class CommandClickImagePosition(CommandMoveToPicPosition):
    def __init__(self):
        super().__init__(set_layout=False)
        """
        ui设置
        """
        self.verticalLayout_line = QVBoxLayout(self)
        self.verticalLayout_line.setSpacing(5)
        self.verticalLayout_line.setContentsMargins(0, 0, 0, 0)

        # 第1列布局
        self.horizontalLayout_line1 = self.ui  # 继承的原有布局

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
        self.label_6.setText('次，每次点击间隔')
        self.horizontalLayout_line2.addWidget(self.label_6)

        self.doubleSpinBox_interval = QDoubleSpinBox()
        self.doubleSpinBox_interval.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_interval.setMaximum(max_interval)
        self.doubleSpinBox_interval.setValue(default_interval)
        self.horizontalLayout_line2.addWidget(self.doubleSpinBox_interval)

        self.label_7 = QLabel()
        self.label_7.setText('秒')
        self.horizontalLayout_line2.addWidget(self.label_7)

        # 合并两列布局
        self.verticalLayout_line.addLayout(self.horizontalLayout_line1)
        self.verticalLayout_line.addLayout(self.horizontalLayout_line2)

        # 初始化
        self.send_args()

        """
        槽函数设置
        """
        self.comboBox_button.currentTextChanged.connect(self.send_args)
        self.spinBox_clicks.valueChanged.connect(self.send_args)
        self.doubleSpinBox_interval.valueChanged.connect(self.send_args)

    def load_args(self, args_dict):
        super().load_args(args_dict)
        """加载参数设置"""
        button = args_dict['button']
        clicks = args_dict['clicks']
        interval = args_dict['interval']
        self.comboBox_button.setCurrentText(button)
        self.spinBox_clicks.setValue(clicks)
        self.doubleSpinBox_interval.setValue(interval)

    def send_args(self):
        """发送参数设置"""
        mode_find_image = self.comboBox_find_model.currentText()
        duration = self.doubleSpinBox_duration.value()
        button = self.comboBox_button.currentText()
        clicks = self.spinBox_clicks.value()
        interval = self.doubleSpinBox_interval.value()
        self.args_dict['mode_find_image'] = mode_find_image
        self.args_dict['duration'] = duration
        self.args_dict['button'] = button
        self.args_dict['clicks'] = clicks
        self.args_dict['interval'] = interval

        image_path_property = self.label_show_pic.property('image_path')
        screenshot_image_path = image_path_property if image_path_property else ''  # 不能是None
        if screenshot_image_path:
            self.args_dict['screenshot_image_path'] = screenshot_image_path

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandClickImagePosition()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
