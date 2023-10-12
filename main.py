from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from ui_main import Ui_MainWindow
from instruct_line_widgets import  *

"""
定义常量
"""
code_command_dict = {'': '',
                     '单击左键':'widget_command_pic',
                     '双击左键':'widget_command_pic',
                     '单击右键':'widget_command_pic',
                     '输入文本':'widget_command_input',
                     '等待':'widget_command_wait',
                     '滚动滚轮':'widget_command_scroll',
                     '热键':'widget_command_hotkey',
                     '自定义命令':'widget_command_custom'}  # 第一个元素留空，用于初始显示


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        初始化
        """
        self.ui.listWidget_instruct_area.setDragEnabled(True)  # 启用拖动功能
        self.ui.listWidget_instruct_area.setDragDropMode(QListWidget.InternalMove)  # 设置拖放模式为内部移动


        """
        连接信号与槽函数
        """

        self.insert_instruct_line_widgets()
        self.insert_instruct_line_widgets()
        self.insert_instruct_line_widgets()
        self.insert_instruct_line_widgets()

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
        list_widget_item.setSizeHint(widget_instruct.sizeHint()*2)  # 设置列表项的大小
        list_widget_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)  # 启用列表项的拖放支持
        self.ui.listWidget_instruct_area.insertItem(index +1,list_widget_item)
        self.ui.listWidget_instruct_area.setItemWidget(list_widget_item,widget_instruct)

        # 设置内部控件属性
        widget_instruct.comboBox_select_command.addItems(code_command_dict)

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
        index = self.get_index_of_current_widgets(self.sender())
        self.ui.listWidget_instruct_area.takeItem(index)







def main():
    app = QApplication()
    app.setStyle('Fusion')
    show_ui = Main()
    show_ui.setWindowIcon(QIcon('./icon/main.ico'))
    # show_ui.setFixedSize(262, 232)
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()