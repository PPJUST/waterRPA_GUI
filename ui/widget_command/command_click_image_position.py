from ui.widget_command.command_base_image_position import *


class CommandClickImagePosition(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.verticalLayout_top = QVBoxLayout(self)
        self.verticalLayout_top.setSpacing(5)
        self.verticalLayout_top.setContentsMargins(0, 0, 0, 0)

        self.ui_move = HBoxLayoutGroup1()  # 第1列布局
        self.ui_move.signal_args_changed.connect(self.check_args)
        self.ui_move.signal_args_changed.connect(self.send_args)
        self.ui_click = HBoxLayoutGroup2()  # 第2列布局
        self.ui_click.signal_args_changed.connect(self.send_args)

        self.verticalLayout_top.addLayout(self.ui_move)
        self.verticalLayout_top.addLayout(self.ui_click)

        """
        初始化
        """
        self.args_dict = default_args_dict.copy()
        self.send_args()

    def load_args(self, args_dict):
        """加载参数设置"""
        self.args_dict = args_dict
        duration = args_dict['duration']
        mode_find_image = args_dict['mode_find_image']
        screenshot_image_path = args_dict['screenshot_image_path']
        button = args_dict['button']
        clicks = args_dict['clicks']
        interval = args_dict['interval']
        self.ui_move.doubleSpinBox_duration.setValue(duration)
        self.ui_move.comboBox_find_model.setCurrentText(mode_find_image)

        if screenshot_image_path and os.path.exists(screenshot_image_path) and filetype.is_image(screenshot_image_path):
            self.ui_move.choose_pic(screenshot_image_path)

        self.ui_click.comboBox_button.setCurrentText(button)
        self.ui_click.spinBox_clicks.setValue(clicks)
        self.ui_click.doubleSpinBox_interval.setValue(interval)

    def check_args(self):
        """检查参数规范"""
        pic_file = self.ui_move.label_show_pic.property('image_path')
        if not pic_file or not os.path.exists(pic_file) or not filetype.is_image(pic_file):
            self.args_dict['args_all_right'] = False
            self.ui_move.label_show_pic.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.ui_move.label_show_pic.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        mode_find_image = self.ui_move.comboBox_find_model.currentText()
        duration = self.ui_move.doubleSpinBox_duration.value()
        button = self.ui_click.comboBox_button.currentText()
        clicks = self.ui_click.spinBox_clicks.value()
        interval = self.ui_click.doubleSpinBox_interval.value()
        self.args_dict['mode_find_image'] = mode_find_image
        self.args_dict['duration'] = duration
        self.args_dict['button'] = button
        self.args_dict['clicks'] = clicks
        self.args_dict['interval'] = interval

        image_path_property = self.ui_move.label_show_pic.property('image_path')
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
