class command_widget_screenshot_area(QWidget):
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
        max_x = default_args_dict_copy['max_x']
        max_y = default_args_dict_copy['max_y']
        default_area = default_args_dict_copy['default_area']
        default_pic_file = default_args_dict_copy['default_pic_file']
        """
        ui设置
        """
        self.horizontalLayout = QHBoxLayout(self)

        self.label_2 = QLabel()
        self.label_2.setText('对 (x1:')
        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_xl = QSpinBox()
        self.spinBox_xl.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_xl.setMaximum(max_x)
        self.spinBox_xl.setValue(default_area[0])
        self.horizontalLayout.addWidget(self.spinBox_xl)

        self.label_3 = QLabel()
        self.label_3.setText(',y1:')
        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_yl = QSpinBox()
        self.spinBox_yl.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_yl.setMaximum(max_y)
        self.spinBox_yl.setValue(default_area[1])
        self.horizontalLayout.addWidget(self.spinBox_yl)

        self.label_4 = QLabel()
        self.label_4.setText(',x2:')
        self.horizontalLayout.addWidget(self.label_4)

        self.spinBox_xr = QSpinBox()
        self.spinBox_xr.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_xr.setMaximum(max_x)
        self.spinBox_xr.setValue(default_area[2])
        self.horizontalLayout.addWidget(self.spinBox_xr)

        self.label_5 = QLabel()
        self.label_5.setText(',y2:')
        self.horizontalLayout.addWidget(self.label_5)

        self.spinBox_yr = QSpinBox()
        self.spinBox_yr.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_yr.setMaximum(max_y)
        self.spinBox_yr.setValue(default_area[3])
        self.horizontalLayout.addWidget(self.spinBox_yr)

        self.label_6 = QLabel()
        self.label_6.setText(') 区域截图，并保存图片至')
        self.horizontalLayout.addWidget(self.label_6)

        self.lineEdit_pic_file = QLineEdit()
        self.lineEdit_pic_file.setPlaceholderText('输入文件名（不含后缀），如存在则覆盖')
        if default_pic_file:
            self.lineEdit_pic_file.setText(default_pic_file)
        self.horizontalLayout.addWidget(self.lineEdit_pic_file)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.horizontalLayout.addWidget(self.line)

        self.toolButton_locate = QToolButton()
        self.toolButton_locate.setText('定位')
        self.horizontalLayout.addWidget(self.toolButton_locate)

        """
        初始化
        """
        self.right_args_filename = False
        self.right_args_xy = False
        self.check_args_filename()
        self.check_args_xy()
        self.send_args()

        """
        槽函数设置
        """
        self.lineEdit_pic_file.textChanged.connect(self.check_args_filename)
        self.spinBox_xl.valueChanged.connect(self.check_args_xy)
        self.spinBox_yl.valueChanged.connect(self.check_args_xy)
        self.spinBox_xr.valueChanged.connect(self.check_args_xy)
        self.spinBox_yr.valueChanged.connect(self.check_args_xy)

        self.lineEdit_pic_file.textChanged.connect(self.send_args)
        self.spinBox_xl.valueChanged.connect(self.send_args)
        self.spinBox_yl.valueChanged.connect(self.send_args)
        self.spinBox_xr.valueChanged.connect(self.send_args)
        self.spinBox_yr.valueChanged.connect(self.send_args)

        self.toolButton_locate.clicked.connect(self.screenshot)

    def screenshot(self):
        """截屏"""
        dialog = qdialog_screenshot.QDialogScreenshot()
        dialog.signal_screenshot_area.connect(dialog.close)  # 先关闭dialog再进行截图，防止将遮罩也截入
        dialog.signal_screenshot_area.connect(self.get_screenshot_area)
        dialog.exec_()

    def get_screenshot_area(self, screenshot_area: list):
        """获取截屏区域的信号"""
        x_start, y_start, x_end, y_end = screenshot_area
        self.spinBox_xl.setValue(x_start)
        self.spinBox_yl.setValue(y_start)
        self.spinBox_xr.setValue(x_end)
        self.spinBox_yr.setValue(y_end)

    def check_args_filename(self):
        """检查参数规范"""
        pic_file = self.lineEdit_pic_file.text().strip()
        if not pic_file or not check_filename_feasible(pic_file):
            self.right_args_filename = False
            self.lineEdit_pic_file.setStyleSheet(error_stylesheet_border)
        else:

            self.right_args_filename = True
            self.lineEdit_pic_file.setStyleSheet('')

    def check_args_xy(self):
        """检查参数规范"""
        x_1 = self.spinBox_xl.value()
        y_1 = self.spinBox_yl.value()
        x_2 = self.spinBox_xr.value()
        y_2 = self.spinBox_yr.value()

        if x_1 == x_2:
            check_x = False
            self.spinBox_xl.setStyleSheet(error_stylesheet_border)
            self.spinBox_xr.setStyleSheet(error_stylesheet_border)
        else:
            check_x = True
            self.spinBox_xl.setStyleSheet('')
            self.spinBox_xr.setStyleSheet('')

        if y_1 == y_2:
            check_y = False
            self.spinBox_yl.setStyleSheet(error_stylesheet_border)
            self.spinBox_yr.setStyleSheet(error_stylesheet_border)
        else:
            check_y = True
            self.spinBox_yl.setStyleSheet('')
            self.spinBox_yr.setStyleSheet('')

        if check_x and check_y:
            self.right_args_xy = True
        else:
            self.right_args_xy = False

    def send_args(self):
        """发送参数设置"""
        if self.right_args_filename and self.right_args_xy:
            right_args = True
        else:
            right_args = False

        pic_file_name = self.lineEdit_pic_file.text().strip()
        if pic_file_name:
            pic_file_suffix = '.png'
        else:
            pic_file_suffix = ''
        pic_file = pic_file_name + pic_file_suffix

        x_1 = self.spinBox_xl.value()
        y_1 = self.spinBox_yl.value()
        x_2 = self.spinBox_xr.value()
        y_2 = self.spinBox_yr.value()
        xl, xr = sorted([x_1, x_2])
        yl, yr = sorted([y_1, y_2])
        area = (xl, yl, xr, yr)

        args_dict = {'right_args': right_args,
                     'pic_file': pic_file,
                     'area': area}

        self.signal_args.emit(args_dict)
