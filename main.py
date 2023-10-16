import os

from instruct_function import *
from instruct_line_widgets import *
from ui_main import Ui_MainWindow


# 备忘录 各种指令用画表的方法统一格式，使得只需要修改一处地方代码就可以统一全部方案



"""
定义常量
"""
icon_edit = r'icon/edit.png'
icon_error = r'icon/error.png'
icon_right = r'icon/right.png'




class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        初始化
        """
        self.check_default_config()
        self.ui.listWidget_instruct_area.setDragEnabled(True)  # 启用拖动功能
        self.ui.listWidget_instruct_area.setDragDropMode(QListWidget.InternalMove)  # 设置拖放模式为内部移动
        self.insert_instruct_line_widgets()  # 生成一个初始控件组
        pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常

        self.instruct_setting = dict()  # 存放各个命令行的参数设置，格式为{命令行id:{args_dict数据},...}
        """
        连接信号与槽函数
        """
        # 配置文件区

        # 功能区
        self.ui.pushButton_start.clicked.connect(self.start_instruct)
        self.ui.pushButton_stop.clicked.connect(self.stop_instruct)

    def get_args(self,args_dict):
        instruct_id = self.sender().property('id')
        self.instruct_setting[instruct_id] = args_dict

    def insert_instruct_line_widgets(self):
        """插入指令行控件组
        传参：sender 即self.sender()"""
        # 计算当前索引
        if self.sender():
            index = self.get_index_of_current_widgets(self.sender())
        else:
            index = self.ui.listWidget_instruct_area.count()

        # 在当前索引后插入新的控件组
        widget_instruct = WidgetInstructLine()
        widget_instruct.setProperty('id', create_random_string(16))  # 设置命令行控件组的唯一id
        list_widget_item = QListWidgetItem()
        list_widget_item.setSizeHint(widget_instruct.sizeHint() * 2)  # 设置列表项的大小
        list_widget_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)  # 启用列表项的拖放支持
        self.ui.listWidget_instruct_area.insertItem(index + 1, list_widget_item)
        self.ui.listWidget_instruct_area.setItemWidget(list_widget_item, widget_instruct)

        # 内部控件连接槽函数
        widget_instruct.toolButton_add_instruct.clicked.connect(self.insert_instruct_line_widgets)
        widget_instruct.toolButton_delete_instruct.clicked.connect(self.delete_instruct_line_widgets)

        widget_instruct.signal_send_args.connect(self.get_args)




    def get_index_of_current_widgets(self, sender,position='in_instruct'):
        """获取当前操作的控件在控件区中的索引号
        传参：
        sender 即self.sender()
        position 控件位置，外部的指令行控件组'instruct'，或控件组内部控件'in_instruct'"""
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
        total_command_number = self.ui.listWidget_instruct_area.count()

        for i in range(total_command_number):
            item = self.ui.listWidget_instruct_area.item(i)
            instruct_widget = self.ui.listWidget_instruct_area.itemWidget(item)  # 获取控件组对象
            command_type = instruct_widget.comboBox_select_command.currentText()  # 获取指令中文名
            instruct_id = instruct_widget.property('id')  # 获取控件组id
            instruct_funciton = code_command_dict[command_type]['function']  # 查表获取完整函数str
            instruct_data = self.instruct_setting[instruct_id]  # 根据id获取参数str

            # 将字典项转换为变量，用于后续调用函数
            for key in instruct_data:
                value = instruct_data[key]
                if type(value) is str:
                    exec(f"{key}='{value}'")
                else:
                    exec(f'{key}={value}')
                print((f'{key}={value}'))

            # 调用对应函数，相关变量已使用exec创建
            exec(f'{instruct_funciton}')



    def stop_instruct(self):
        """中止指令"""
        pyautogui.moveTo(0, 0)

    def check_default_config(self):
        """检查初始配置文件"""
        if not os.path.exists('config') or not os.listdir('config'):
            os.makedirs('config/默认')
            with open('config/默认/setting.ini', 'w', encoding='utf-8') as sw:
                setting = """[DEFAULT]
loop_time = 1"""
                sw.write(setting)


def main():
    app = QApplication()
    app.setStyle('Fusion')
    show_ui = Main()
    show_ui.setWindowIcon(QIcon('./icon/main.ico'))
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()