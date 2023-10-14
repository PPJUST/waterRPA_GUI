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


code_command_dict = {'': '',
                     '单击左键': 'widget_command_pic',
                     '双击左键': 'widget_command_pic',
                     '单击右键': 'widget_command_pic',
                     '输入文本': 'widget_command_input',
                     '等待时间': 'widget_command_wait',
                     '等待时间(随机)': 'widget_command_wait',
                     '滚动滚轮': 'widget_command_scroll',
                     '模拟按键': 'widget_command_hotkey',
                     '自定义命令': 'widget_command_custom'}  # 第一个元素留空，用于初始显示
# 备忘录 修改文本描述 区分鼠标、键盘、图像操作

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

        """
        连接信号与槽函数
        """
        # 配置文件区

        # 功能区
        self.ui.pushButton_start.clicked.connect(self.start_instruct)
        self.ui.pushButton_stop.clicked.connect(self.stop_instruct)

    def insert_instruct_line_widgets(self):
        """插入指令行控件组
        传参：sender 即self.sender()"""
        # 计算当前索引
        if self.sender():
            index = self.get_index_of_current_widgets(self.sender())
        else:
            index = self.ui.listWidget_instruct_area.count()

        # 在当前索引后插入新的控件组
        widget_instruct = widget_instruct_line()
        list_widget_item = QListWidgetItem()
        list_widget_item.setSizeHint(widget_instruct.sizeHint() * 2)  # 设置列表项的大小
        list_widget_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)  # 启用列表项的拖放支持
        self.ui.listWidget_instruct_area.insertItem(index + 1, list_widget_item)
        self.ui.listWidget_instruct_area.setItemWidget(list_widget_item, widget_instruct)

        # 设置内部控件属性
        widget_instruct.comboBox_select_command.addItems(code_command_dict)
        # 设置状态label的图标
        pixmap = QPixmap(icon_edit)
        resize = calculate_resize(widget_instruct.label_state.size(), pixmap.size())
        pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
        widget_instruct.label_state.setPixmap(pixmap)




        # 内部控件连接槽函数
        widget_instruct.toolButton_add_instruct.clicked.connect(self.insert_instruct_line_widgets)
        widget_instruct.toolButton_delete_instruct.clicked.connect(self.delete_instruct_line_widgets)

    def get_index_of_current_widgets(self, sender):
        """获取当前操作的控件在控件区中的索引号
        传参：sender 即self.sender()"""
        parent_widget = sender.parentWidget()

        for i in range(self.ui.listWidget_instruct_area.count()):
            item = self.ui.listWidget_instruct_area.item(i)
            item_widget = self.ui.listWidget_instruct_area.itemWidget(item)

            if item_widget is parent_widget:
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
            item_widget = self.ui.listWidget_instruct_area.itemWidget(item)
            command_type = item_widget.comboBox_select_command.currentText()
            command_widget = item_widget.widget_command_setting.layout().itemAt(0).widget()
            print(command_widget)
            # 备忘录 后期优化
            time.sleep(0.1)  # 每个指令键暂停0.1秒
            if command_type == '单击左键':
                click_time = 1
                l_or_r_click = 'left'
                pic_file = command_widget.label_show_pic.property('pic_path')  # 图片的路径存放在property中
                instruct_pic_click(click_time, l_or_r_click, pic_file)
            elif command_type == '双击左键':
                click_time = 2
                l_or_r_click = 'left'
                pic_file = command_widget.label_show_pic.property('pic_path')
                print(pic_file)
                instruct_pic_click(click_time, l_or_r_click, pic_file)
            elif command_type == '单击右键':
                click_time = 1
                l_or_r_click = 'right'
                pic_file = command_widget.label_show_pic.property('pic_path')
                instruct_pic_click(click_time, l_or_r_click, pic_file)
            elif command_type == '输入文本':
                text = command_widget.lineEdit_input.text()
                instruct_input(text)
            elif command_type == '等待时间':
                wait_time = command_widget.doubleSpinBox_wait_second.value()
                instruct_wait(wait_time)
            elif command_type == '等待时间(随机)':
                pass
            elif command_type == '滚动滚轮':
                direction = command_widget.comboBox_scroll_direction.currentText()
                distance = command_widget.spinBox_scroll_distance.value()
                instruct_scroll(direction, distance)
            elif command_type == '模拟按键':
                hotkey_str = command_widget.lineEdit_hotkey.text()
                instruct_hotkey(hotkey_str)
            elif command_type == '自定义命令':
                pass

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
