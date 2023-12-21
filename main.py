from module.function_general import *
from module.thread_run_commands import *
from ui.ui_main import Ui_MainWindow
from ui.widget_command_control import *
from ui.widget_listener import *
from ui.widget_moved_list_widget import *

"""
行项目id data：1
控件组id property：'id'
"""


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        控件设置
        """
        # 添加自定义listwidget控件
        layout = self.ui.groupBox_command.layout()
        self.listWidget_command_area = MovedListWidget()
        layout.addWidget(self.listWidget_command_area)
        self.listWidget_command_area.setDragEnabled(True)  # 启用拖动功能
        self.listWidget_command_area.setDragDropMode(QListWidget.InternalMove)  # 设置拖放模式为内部移动
        self.listWidget_command_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁止水平滚动条
        self.listWidget_command_area.setDefaultDropAction(Qt.TargetMoveAction)
        self.listWidget_command_area.itemMoved.connect(self.command_item_moved)

        """
        连接信号与槽函数
        """
        # 配置文件区
        self.ui.toolButton_add_config.clicked.connect(self.add_config)
        self.ui.toolButton_delete_config.clicked.connect(self.delete_config)
        self.ui.toolButton_save_config.clicked.connect(self.save_command_setting)
        self.ui.comboBox_select_config.currentTextChanged.connect(self.load_config_command)
        # 功能区
        self.ui.pushButton_start.clicked.connect(self.reset_runs_times)
        self.ui.pushButton_start.clicked.connect(self.run_commands)
        self.ui.pushButton_stop.clicked.connect(self.stop_run_commands)
        self.ui.pushButton_listener.clicked.connect(self.start_listener)
        # 全局设置区
        self.ui.doubleSpinBox_global_wait_time.valueChanged.connect(function_config.update_config_wait_time)
        self.ui.spinBox_loop_time.valueChanged.connect(function_config.update_config_loop_time)

        """
        初始设置
        """
        self.command_dict = dict()  # 各个命令行的参数设置，格式为{命令行id:{args_dict数据},...}
        function_config.check_default_config()
        pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常
        pyautogui.PAUSE = 0  # pyautogui自带的延迟功能，默认延迟时间0.1秒，不使用该自带功能而使用time.sleep进行延迟时间的设置
        self.runs_times = 0  # 已运行次数，用于循环运行
        self.load_global_setting()  # 加载全局设置

        """
        多线程设置
        """
        self.thread_run_command = ThreadRunCommands()
        self.thread_run_command.signal_succeed.connect(self.run_commands_succeed)
        self.thread_run_command.signal_failed.connect(self.run_commands_failed)
        self.thread_run_command.signal_succeed.connect(self.scroll_to_item)
        self.thread_run_command.signal_failed.connect(self.scroll_to_item)
        self.thread_run_command.signal_finished.connect(self.run_commands_finished)
        self.thread_run_command.signal_error.connect(self.run_commands_error)

    """
    执行相关函数
    """

    def check_command_all_right(self):
        """检查存储的指令参数设置，判断是否启用执行按钮"""
        self.ui.pushButton_start.setEnabled(True)
        for args in self.command_dict.values():
            if args:  # 不考虑空的键值对
                args_all_right = args['args_all_right']
                if not args_all_right:
                    self.ui.pushButton_start.setEnabled(False)
                    break

    def get_args_signal(self, args_dict):
        """接收子控件传递的信号"""
        id_widget = self.sender().property('id')
        self.command_dict[id_widget] = args_dict
        self.check_command_all_right()
        # self.save_command_setting()  # 每次更新保存配置

    def run_commands(self):
        """执行指令"""
        # 执行前保存配置文件
        self.save_command_setting()
        # 重置图标
        self.reset_state_icon()
        # 禁用控件
        self.change_widget_enable(False)
        # 获取每个行项目对应的指令函数
        command_function_dict = {}  # {id:对应function,...}
        total_command_number = self.listWidget_command_area.count()
        for i in range(total_command_number):
            item = self.listWidget_command_area.item(i)
            id_item = item.data(1)
            args_dict = self.command_dict[id_item]
            command_type = args_dict['command_type']
            convert = CommandConvert(command_type)
            command_function = convert.get_function_object(args_dict)
            command_function_dict[id_item] = command_function
        # 子线程中执行
        self.thread_run_command.set_command_function(command_function_dict)
        self.thread_run_command.start()

    def stop_run_commands(self):
        """终止指令"""
        self.change_widget_enable(True)
        pyautogui.moveTo(0, 0)

    def change_widget_enable(self, enable=True):
        """执行或结束时启用或禁用相关控件"""
        if enable:
            # 配置文件
            self.ui.comboBox_select_config.setEnabled(True)
            self.ui.toolButton_save_config.setEnabled(True)
            self.ui.toolButton_add_config.setEnabled(True)
            self.ui.toolButton_delete_config.setEnabled(True)
            # 全局设置
            self.ui.doubleSpinBox_global_wait_time.setEnabled(True)
            self.ui.spinBox_loop_time.setEnabled(True)
            self.ui.spinBox_find_image_timeout.setEnabled(True)
            # 执行
            self.ui.pushButton_start.setEnabled(True)
            self.ui.pushButton_stop.setEnabled(False)
        else:
            # 配置文件
            self.ui.comboBox_select_config.setEnabled(False)
            self.ui.toolButton_save_config.setEnabled(False)
            self.ui.toolButton_add_config.setEnabled(False)
            self.ui.toolButton_delete_config.setEnabled(False)
            # 全局设置
            self.ui.doubleSpinBox_global_wait_time.setEnabled(False)
            self.ui.spinBox_loop_time.setEnabled(False)
            self.ui.spinBox_find_image_timeout.setEnabled(False)
            # 执行
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(True)

    def reset_state_icon(self):
        """重置状态图标"""
        total_command_number = self.listWidget_command_area.count()

        for i in range(total_command_number):
            item = self.listWidget_command_area.item(i)
            widget = self.listWidget_command_area.itemWidget(item)  # 获取控件组对象
            widget.toolButton_state.setIcon(QIcon(icon_wait_run))  # 修改状态的图标-执行

    """
    接收多线程信号相关函数
    """

    def scroll_to_item(self, id_run):
        """滚动行项目到执行行"""
        for i in range(self.listWidget_command_area.count()):
            item = self.listWidget_command_area.item(i)
            widget = self.listWidget_command_area.itemWidget(item)
            id_widget = widget.property('id')

            if id_widget == id_run:
                try:
                    scroll_to = self.listWidget_command_area.item(i + 2)  # 滚动到下面第二行
                    self.listWidget_command_area.scrollToItem(scroll_to)
                    break
                except:
                    break

    def run_commands_succeed(self, id_succeed):
        """修改成功运行的行项目图标"""
        for i in range(self.listWidget_command_area.count()):
            item = self.listWidget_command_area.item(i)
            widget = self.listWidget_command_area.itemWidget(item)
            id_widget = widget.property('id')

            if id_widget == id_succeed:
                widget.toolButton_state.setIcon(QIcon(icon_complete))  # 修改状态的图标-完成
                break

    def run_commands_failed(self, id_failed):
        """修改运行失败的行项目图标"""
        for i in range(self.listWidget_command_area.count()):
            item = self.listWidget_command_area.item(i)
            widget = self.listWidget_command_area.itemWidget(item)
            id_widget = widget.property('id')

            if id_widget == id_failed:
                widget.toolButton_state.setIcon(QIcon(icon_error))  # 修改状态的图标-完成
                break

    def run_commands_error(self, error_message):
        """处理子线程的报错信息"""
        QMessageBox.warning(self, "错误", f"错误信息：【{error_message}】")

    def run_commands_finished(self, result_code):
        """全部行项目运行结束后，检查是否需要循环运行"""
        if result_code:
            self.runs_times += 1
            loop_time = self.ui.spinBox_loop_time.value()
            if loop_time == 0:
                self.run_commands()
            else:
                if self.runs_times < loop_time:
                    self.run_commands()
                else:
                    self.change_widget_enable(True)
        else:
            self.change_widget_enable(True)

    """
    命令控件相关函数
    """

    def load_config_command(self):
        """加载配置文件中的命令控件"""
        # 重置
        self.command_dict = dict()
        self.listWidget_command_area.clear()

        # 添加
        config = self.ui.comboBox_select_config.currentText()
        command_list = function_config.get_command_list(config)
        for args_dict in command_list:
            self.insert_command_widget(args_dict=args_dict)

        # 如果命令行为空，则插入空行
        if self.listWidget_command_area.count() == 0:
            self.insert_command_widget()

    def insert_command_widget(self, args_dict: dict = None, index: int = None):
        """插入指令行控件
        传参：
        args_dict 指令设置的字典，用于初始传参
        sender 即self.sender()"""
        # 随机一个id，并添加入字典
        id_random = create_random_string(8)
        self.command_dict[id_random] = {}  # 创建对应的空键值对

        # 计算当前索引
        if index is None:
            if self.sender():
                index = self.get_widget_index(self.sender())
                if index is None:
                    index = self.listWidget_command_area.count()
            else:
                index = self.listWidget_command_area.count()

        # 如果传入args为空，则写入默认字典
        if not args_dict:
            args_dict = default_args_dict.copy()

        # 在当前索引后插入新的控件组
        child_widget = WidgetCommandControl()
        child_widget.load_command_args(args_dict)
        child_widget.setProperty('id', id_random)  # 设置控件组的唯一id

        list_widget_item = QListWidgetItem()
        list_widget_item.setData(1, id_random)  # 设置行项目相同的id
        resize = QSize(self.sizeHint().width(), 100)
        list_widget_item.setSizeHint(resize)
        list_widget_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)  # 启用列表项的拖放支持

        self.listWidget_command_area.insertItem(index + 1, list_widget_item)
        self.listWidget_command_area.setItemWidget(list_widget_item, child_widget)

        # 设置行项目的边框
        self.listWidget_command_area.setStyleSheet("QListWidget::item { border: 1px solid grey; }")

        # 内部控件连接槽函数
        child_widget.toolButton_add_command.clicked.connect(self.insert_command_widget)
        child_widget.toolButton_copy_command.clicked.connect(self.copy_command_widget)
        child_widget.toolButton_delete_command.clicked.connect(self.delete_command_widget)
        child_widget.signal_send_args.connect(self.get_args_signal)
        child_widget.get_command_signal(args_dict)  # 手工执行一次，防止添加时不更新

    def copy_command_widget(self):
        """复制指令行控件"""
        # 提取复制项的参数设置
        parent = self.sender().parentWidget()
        id_widget = parent.property('id')
        args_dict = self.command_dict[id_widget]

        # 插入复制的行
        self.insert_command_widget(args_dict=args_dict)

    def delete_command_widget(self):
        """删除指令行控件"""
        # 如果删除的是最后一个控件组，则先新增一个空白的再删除
        if self.listWidget_command_area.count() == 1:
            self.insert_command_widget()

        # 获取行项目对象
        index = self.get_widget_index(self.sender())  # 获取索引
        list_item = self.listWidget_command_area.item(index)  # 获取行项目对象
        list_widget = self.listWidget_command_area.itemWidget(list_item)  # 获取控件对象
        id_widget = list_widget.property('id')

        # 删除
        self.command_dict.pop(id_widget)
        self.listWidget_command_area.takeItem(index)

        # 重新检查参数规范
        self.check_command_all_right()

        # 保存一遍配置
        self.save_command_setting()

    def command_item_moved(self):
        """移动行项目后的处理"""
        error_index = None
        error_id = None
        for index in range(self.listWidget_command_area.count()):
            item = self.listWidget_command_area.item(index)
            item_widget = self.listWidget_command_area.itemWidget(item)
            try:
                item_widget.property("id")
            except AttributeError:
                error_index = index
                error_id = item.data(1)
                break

        if error_index:
            # 删除错误行项目
            error_item = self.listWidget_command_area.takeItem(error_index)
            del error_item
            # 添加新的行项目
            args_dict = self.command_dict[error_id]
            if error_index == 1:  # 第1行出错时，插入行项目的index需要为0
                error_index = 0
            self.insert_command_widget(index=error_index - 1, args_dict=args_dict)
            # 删除错误id
            self.command_dict.pop(error_id)

    def get_widget_index(self, sender):
        """获取当前操作的控件在控件区中的索引号
        传参：
        sender 即self.sender()"""
        parent = sender.parentWidget()
        for index in range(self.listWidget_command_area.count()):
            item = self.listWidget_command_area.item(index)
            item_widget = self.listWidget_command_area.itemWidget(item)

            if item_widget is parent:
                return index

    """
    配置文件相关函数
    """

    def load_global_setting(self):
        """加载全局设置"""
        # 加载设置项
        config_list = function_config.get_config_items()
        if not config_list:
            config_list = ['默认']
            function_config.add_config('默认')
        self.ui.comboBox_select_config.addItems(config_list)
        # 加载循环次数
        loop_time = function_config.get_config_loop_time()
        self.ui.spinBox_loop_time.setValue(loop_time)
        # 加载指令间隔
        wait_time = function_config.get_config_wait_time()
        self.ui.doubleSpinBox_global_wait_time.setValue(wait_time)

    def reset_runs_times(self):
        """重置已运行次数"""
        self.runs_times = 0

    def add_config(self):
        """新建配置文件"""
        config_name, _ = QInputDialog.getText(self, "新建配置文件", "名称:", text="默认")
        if config_name:
            checked_config = function_config.add_config(config_name)
            self.ui.comboBox_select_config.addItem(checked_config)
            self.ui.comboBox_select_config.setCurrentText(checked_config)

    def delete_config(self):
        """删除配置文件"""
        config_name = self.ui.comboBox_select_config.currentText()
        config_index = self.ui.comboBox_select_config.currentIndex()
        # 弹出确认对话框
        reply = QMessageBox.warning(self, "删除配置文件", f"是否删除【{config_name}】", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            function_config.delete_config(config_name)
            self.ui.comboBox_select_config.setCurrentIndex(0)
            self.ui.comboBox_select_config.removeItem(config_index)

        if self.ui.comboBox_select_config.count() == 0:
            self.add_config()

    def save_command_setting(self):
        """保存配置文件的设置项"""
        config = self.ui.comboBox_select_config.currentText()
        command_data_dict = {}  # 结构：{id:{args_dict字典}, ...}

        total_command_number = self.listWidget_command_area.count()
        for i in range(total_command_number):
            item = self.listWidget_command_area.item(i)
            widget = self.listWidget_command_area.itemWidget(item)
            try:
                id_widget = widget.property('id')  # 获取控件组id
            except AttributeError:
                id_widget = item.data(1)
            args_dict = self.command_dict[id_widget]  # 根据id获取args字典
            if id_widget not in command_data_dict:
                command_data_dict[id_widget] = args_dict

        command_list = list(command_data_dict.values())
        function_config.save_command_config(config, command_list)

    """
    键鼠录制相关函数
    """

    def start_listener(self):
        """开始监听"""
        reply = QMessageBox.warning(self, "监听器", f"是否开始录制键鼠操作", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.dialog = DialogListener()
            self.dialog.signal_send_listener.connect(self.get_listener_data)
            self.dialog.show()

    def get_listener_data(self, listener_list):
        """接收录制操作的数据，保存配置文件后重新读取更新ui"""
        config = self.ui.comboBox_select_config.currentText()
        function_config.save_command_config(config, listener_list)
        self.load_config_command()


def main():
    app = QApplication()
    app.setStyle('Fusion')
    show_ui = Main()
    show_ui.setWindowIcon(QIcon('./icon/main.ico'))
    show_ui.show()
    app.exec()


if __name__ == "__main__":
    main()
