import configparser
import string

import send2trash
from PySide2.QtWidgets import QMainWindow, QListWidgetItem, QListWidget, QInputDialog

from instruct_function import *
from instruct_line_widgets import *
from ui_main import Ui_MainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        初始化
        """
        self.instruct_setting = dict()  # 存放各个命令行的参数设置，格式为{命令行id:{args_dict数据},...}
        self.check_default_config()
        self.ui.listWidget_instruct_area.setDragEnabled(True)  # 启用拖动功能
        self.ui.listWidget_instruct_area.setDragDropMode(QListWidget.InternalMove)  # 设置拖放模式为内部移动

        pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常
        self.load_config_to_combobox()  # 加载配置文件到comboBox
        if self.ui.listWidget_instruct_area.count() == 0:
            self.insert_instruct_line_widgets()  # 生成一个初始控件组

        """
        连接信号与槽函数
        """
        # 配置文件区
        self.ui.toolButton_save_config.clicked.connect(self.save_config)
        self.ui.toolButton_add_config.clicked.connect(self.add_config)
        self.ui.toolButton_delete_config.clicked.connect(self.delete_config)
        self.ui.comboBox_select_config.currentTextChanged.connect(self.load_instruct)
        # 功能区
        self.ui.pushButton_start.clicked.connect(self.start_instruct)
        self.ui.pushButton_stop.clicked.connect(self.stop_instruct)

    def get_args(self, args_dict):
        """接收传递的信号"""
        instruct_id = self.sender().property('id')
        self.instruct_setting[instruct_id] = args_dict

        # 是否启用执行按钮
        self.ui.pushButton_start.setEnabled(True)
        for i_dict in self.instruct_setting.values():
            if i_dict:  # 不考虑空的键值对
                right_args = i_dict['right_args']
                if not right_args:
                    self.ui.pushButton_start.setEnabled(False)

    def load_instruct(self):
        """加载命令行设置"""
        self.ui.listWidget_instruct_area.clear()
        current_config = self.ui.comboBox_select_config.currentText()
        config = configparser.ConfigParser()
        config.read(f'config/{current_config}/setting.ini', encoding='utf-8')  # 配置文件的路径
        for section in config.sections():
            args_dict_config = {}
            keys = config.options(section)
            for key in keys:
                args_dict_config[key] = config.get(section, key)

            self.insert_instruct_line_widgets(args_dict_config)

        if self.ui.listWidget_instruct_area.count() == 0:
            self.insert_instruct_line_widgets()

    def insert_instruct_line_widgets(self, args_dict_config=None):
        """插入指令行控件组
        传参：
        args_dict_config 指令设置的字典，用于初始化
        sender 即self.sender()"""
        # 计算当前索引
        if self.sender():
            index = self.get_index_of_current_widgets(self.sender())
            if index is None:
                index = self.ui.listWidget_instruct_area.count()
        else:
            index = self.ui.listWidget_instruct_area.count()

        # 在当前索引后插入新的控件组
        widget_instruct = WidgetInstructLine(args_dict_config)
        id_random = create_random_string(16)
        widget_instruct.setProperty('id', id_random)  # 设置命令行控件组的唯一id
        self.instruct_setting[id_random] = {}  # 创建对应的空键值对
        list_widget_item = QListWidgetItem()
        list_widget_item.setSizeHint(widget_instruct.sizeHint() * 2)  # 设置列表项的大小
        list_widget_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)  # 启用列表项的拖放支持
        self.ui.listWidget_instruct_area.insertItem(index + 1, list_widget_item)
        self.ui.listWidget_instruct_area.setItemWidget(list_widget_item, widget_instruct)

        # 内部控件连接槽函数
        widget_instruct.toolButton_add_instruct.clicked.connect(self.insert_instruct_line_widgets)
        widget_instruct.toolButton_delete_instruct.clicked.connect(self.delete_instruct_line_widgets)

        widget_instruct.signal_send_args.connect(self.get_args)
        if args_dict_config:
            widget_instruct.child_widget_command.send_args()  # 手工执行一次子控件的发送信号函数，用于初始化

    def get_index_of_current_widgets(self, sender, position='in_instruct'):
        """获取当前操作的控件在控件区中的索引号
        传参：
        sender 即self.sender()
        position 控件位置，外部的指令行控件组 'instruct'，或控件组内部控件'in_instruct'"""
        if position == 'in_instruct':
            instruct_widget = sender.parentWidget()
        else:
            instruct_widget = sender

        for i in range(self.ui.listWidget_instruct_area.count()):
            item = self.ui.listWidget_instruct_area.item(i)
            item_widget = self.ui.listWidget_instruct_area.itemWidget(item)

            if item_widget is instruct_widget:
                print(f'当前操作的控件在控件区中的索引号：{i}')
                return i

    def delete_instruct_line_widgets(self):
        """删除当前控件组"""
        if self.ui.listWidget_instruct_area.count() == 1:  # 如果删除的是最后一个控件组，则先新增一个空白的再删除
            self.insert_instruct_line_widgets()

        index = self.get_index_of_current_widgets(self.sender())
        self.ui.listWidget_instruct_area.takeItem(index)

    def start_instruct(self):
        """执行指令"""
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)

        total_command_number = self.ui.listWidget_instruct_area.count()

        for i in range(total_command_number):
            item = self.ui.listWidget_instruct_area.item(i)
            instruct_widget = self.ui.listWidget_instruct_area.itemWidget(item)  # 获取控件组对象
            command_type = instruct_widget.comboBox_select_command.currentText()  # 获取指令中文名
            instruct_id = instruct_widget.property('id')  # 获取控件组id
            instruct_function = command_link_dict[command_type]['function']  # 查表获取完整函数str
            instruct_data = self.instruct_setting[instruct_id]  # 根据id获取参数str

            # 将字典项转换为变量，用于后续调用函数
            for key in instruct_data:
                value = instruct_data[key]
                convert = {'左键': 'left', '右键': 'right', '中键': 'middle'}  # 转换为pyautogui支持的文本
                if value in convert:
                    value = convert[value]
                exec(f"{key}='{value}'",globals())

            # 调用对应函数，相关变量已使用exec创建
            print(f'执行函数 {instruct_function}')
            print(f'函数参数 {instruct_data}')
            exec(f'{instruct_function}')

        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def stop_instruct(self):
        """中止指令"""
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

        pyautogui.moveTo(0, 0)

    def load_config_to_combobox(self):
        """加载配置文件到comboBox中显示"""
        configs = os.listdir('config')
        try:
            self.ui.comboBox_select_config.currentTextChanged.disconnect(self.load_instruct)
        except RuntimeError:
            pass
        self.ui.comboBox_select_config.clear()
        self.ui.comboBox_select_config.currentTextChanged.connect(self.load_instruct)
        self.ui.comboBox_select_config.addItems(configs)

    def add_config(self):
        """新建配置文件"""
        configs = os.listdir('config')

        new_config, _ = QInputDialog.getText(self, "新建配置文件", "名称:", text="默认")

        if new_config:
            checked_config = check_filename_feasible(new_config, replace=True)
            if checked_config in configs:  # 如果有重复，则添加随机后缀
                random_string = ''.join(random.choices(string.ascii_lowercase, k=6))
                checked_config = f"{checked_config}_{random_string}"

            os.makedirs(f'config/{checked_config}')

            self.ui.comboBox_select_config.addItem(checked_config)
            self.ui.comboBox_select_config.setCurrentText(checked_config)

    def delete_config(self):
        """删除配置文件"""
        del_config = self.ui.comboBox_select_config.currentText()

        send2trash.send2trash(f'config/{del_config}')
        self.load_config_to_combobox()

    @staticmethod
    def check_default_config():
        """检查初始配置文件"""
        if not os.path.exists('config') or not os.listdir('config'):
            os.makedirs('config/默认')
            with open('config/默认/setting.ini', 'w', encoding='utf-8') as sw:
                setting = """[DEFAULT]
loop_time = 1"""
                sw.write(setting)

    def save_config(self):
        """保存配置文件"""
        config = configparser.ConfigParser()
        path = f'config/{self.ui.comboBox_select_config.currentText()}/setting.ini'
        config.read(path, encoding='utf-8')  # 配置文件的路径
        config.clear()  # 清除全部内容

        total_command_number = self.ui.listWidget_instruct_area.count()

        for i in range(total_command_number):
            item = self.ui.listWidget_instruct_area.item(i)
            instruct_widget = self.ui.listWidget_instruct_area.itemWidget(item)  # 获取控件组对象
            command_type = instruct_widget.comboBox_select_command.currentText()  # 获取指令中文名
            instruct_id = instruct_widget.property('id')  # 获取控件组id
            instruct_data = self.instruct_setting[instruct_id]  # 根据id获取参数str

            config.add_section(str(i))
            config.set(str(i), 'command_type', command_type)

            for key in instruct_data:
                config.set(str(i), str(key), str(instruct_data[key]))

        config.write(open(path, 'w', encoding='utf-8'))


def main():
    app = QApplication()
    app.setStyle('Fusion')
    show_ui = Main()
    show_ui.setWindowIcon(QIcon('./icon/main.ico'))
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()
