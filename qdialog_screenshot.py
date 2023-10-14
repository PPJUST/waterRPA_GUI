from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class FrameSelectWidget(QWidget):
    """自定义QWidget控件
    实现截取区域操作
    发送信号：signal_frame_area(list) 截取区域信号，[开始x轴, 开始y轴, 结束x轴, 结束y轴]
    """
    signal_frame_area = Signal(list)  # 截取区域信号，[开始x轴, 开始y轴, 结束x轴, 结束y轴]
    signal_frame_right_click = Signal()  # 截取时按下右键的信号

    def __init__(self):
        super().__init__()
        # 设置初始变量
        self.state_is_selecting = False  # 框选状态
        self.start_pos = None  # 开始坐标
        self.end_pos = None  # 结束坐标


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 左键按下的操作
            self.state_is_selecting = True
            self.start_pos = event.pos()
            self.end_pos = event.pos()
        elif event.button() == Qt.RightButton:  # 右键按下的操作
            self.signal_frame_right_click.emit()

    def mouseMoveEvent(self, event):
        if self.state_is_selecting:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.state_is_selecting = False

            x_start = self.start_pos.x()
            y_start = self.start_pos.y()
            x_end = self.end_pos.x()
            y_end = self.end_pos.y()
            print(f'选取区域坐标 {[x_start, y_start, x_end, y_end]}')
            self.signal_frame_area.emit([x_start, y_start, x_end, y_end])

            self.start_pos = None
            self.end_pos = None
            self.update()





    def get_selection_rect(self):
        if self.start_pos != self.end_pos:
            return QRect(self.start_pos, self.end_pos).normalized()
        else:
            return QRect(self.start_pos, self.end_pos + QPoint(1, 1)).normalized()

    def paintEvent(self, event):
        if self.state_is_selecting:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(0, 0, 255), 1, Qt.DashLine))
            painter.drawRect(self.get_selection_rect())


class QDialogScreenshot(QDialog):
    """自定义QDialog控件，实现在当前屏幕框选区域进行截图的功能
    发送信号：signal_screenshot_area(list) 截取区域信号，[开始x轴, 开始y轴, 结束x轴, 结束y轴]
    """
    signal_screenshot_area = Signal(list)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(400, 300))

        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 设置全屏+置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 调整大小为全屏
        screen_geometry = QDesktopWidget().screenGeometry()  # screenGeometry为过时方法已弃用，后面再找新的方法
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.setGeometry(0, 0, screen_width, screen_height)
        # 设置半透明
        self.setWindowOpacity(0.5)  # 0~1，0为完全透明
        # 设置布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        widget = FrameSelectWidget()
        widget.signal_frame_area.connect(self.get_signal_frame)
        widget.signal_frame_right_click.connect(self.close)
        layout.addWidget(widget)


    def get_signal_frame(self, frame_area:list):
        self.signal_screenshot_area.emit(frame_area)
        # self.close()  # 退出截图，最好在外部退出，不然会将遮罩也截屏进去




def _test():
    app = QApplication([])
    dialog = QDialogScreenshot()
    dialog.exec_()

if __name__ == '__main__':
    _test()

