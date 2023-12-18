from ui.widget_command.command_base_image_position import *


class CommandMoveToImagePosition(QWidget):
    signal_args = Signal(dict)

    def __init__(self):
        super().__init__()
        """
        ui设置
        """
        self.ui = HBoxLayoutGroup1()
        self.ui.signal_args_changed.connect(self.check_args)
        self.ui.signal_args_changed.connect(self.send_args)
        self.setLayout(self.ui)

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
        self.ui.doubleSpinBox_duration.setValue(duration)
        self.ui.comboBox_find_model.setCurrentText(mode_find_image)

        if screenshot_image_path and os.path.exists(screenshot_image_path) and filetype.is_image(screenshot_image_path):
            self.ui.choose_pic(screenshot_image_path)

    def check_args(self):
        """检查参数规范"""
        pic_file = self.ui.label_show_pic.property('image_path')
        if not pic_file or not os.path.exists(pic_file) or not filetype.is_image(pic_file):
            self.args_dict['args_all_right'] = False
            self.ui.label_show_pic.setStyleSheet(error_stylesheet_border)
        else:
            self.args_dict['args_all_right'] = True
            self.ui.label_show_pic.setStyleSheet('')

    def send_args(self):
        """发送参数设置"""
        mode_find_image = self.ui.comboBox_find_model.currentText()
        duration = self.ui.doubleSpinBox_duration.value()
        self.args_dict['mode_find_image'] = mode_find_image
        self.args_dict['duration'] = duration

        image_path_property = self.ui.label_show_pic.property('image_path')
        screenshot_image_path = image_path_property if image_path_property else ''  # 不能是None
        if screenshot_image_path:
            self.args_dict['screenshot_image_path'] = screenshot_image_path

        self.signal_args.emit(self.args_dict)


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = CommandMoveToImagePosition()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec_()


if __name__ == "__main__":
    _test_widget()
