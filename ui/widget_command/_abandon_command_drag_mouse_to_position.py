class command_widget_drag_mouse_to_position(QWidget):
    signal_args = Signal(dict)

    def __init__(self, args_dict_config=None):
        super().__init__()
        """
        更新初始参数值
        """
        default_args_dict_copy = default_args_dict.copy()
        if args_dict_config:
            for key, value in args_dict_config.items():
                default_args_dict_copy[key] = value
        max_duration = default_args_dict_copy['max_duration']
        default_duration = default_args_dict_copy['default_duration']
        max_x = default_args_dict_copy['max_x']
        default_x = default_args_dict_copy['default_x']
        max_y = default_args_dict_copy['max_y']
        default_y = default_args_dict_copy['default_y']
        default_button = default_args_dict_copy['default_button']

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
