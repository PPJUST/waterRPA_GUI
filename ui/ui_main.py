# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainfXrRtD.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpinBox,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(877, 628)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_config = QGroupBox(self.centralwidget)
        self.groupBox_config.setObjectName(u"groupBox_config")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_config)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.comboBox_select_config = QComboBox(self.groupBox_config)
        self.comboBox_select_config.setObjectName(u"comboBox_select_config")

        self.horizontalLayout_2.addWidget(self.comboBox_select_config)

        self.toolButton_save_config = QToolButton(self.groupBox_config)
        self.toolButton_save_config.setObjectName(u"toolButton_save_config")

        self.horizontalLayout_2.addWidget(self.toolButton_save_config)

        self.toolButton_add_config = QToolButton(self.groupBox_config)
        self.toolButton_add_config.setObjectName(u"toolButton_add_config")

        self.horizontalLayout_2.addWidget(self.toolButton_add_config)

        self.toolButton_delete_config = QToolButton(self.groupBox_config)
        self.toolButton_delete_config.setObjectName(u"toolButton_delete_config")

        self.horizontalLayout_2.addWidget(self.toolButton_delete_config)


        self.verticalLayout_4.addWidget(self.groupBox_config)

        self.groupBox_function = QGroupBox(self.centralwidget)
        self.groupBox_function.setObjectName(u"groupBox_function")
        self.gridLayout = QGridLayout(self.groupBox_function)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_start = QPushButton(self.groupBox_function)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setEnabled(False)

        self.gridLayout.addWidget(self.pushButton_start, 0, 0, 1, 1)

        self.pushButton_stop = QPushButton(self.groupBox_function)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setEnabled(False)

        self.gridLayout.addWidget(self.pushButton_stop, 0, 2, 1, 1)

        self.pushButton_listener = QPushButton(self.groupBox_function)
        self.pushButton_listener.setObjectName(u"pushButton_listener")

        self.gridLayout.addWidget(self.pushButton_listener, 0, 3, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_function)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.groupBox_info = QGroupBox(self.centralwidget)
        self.groupBox_info.setObjectName(u"groupBox_info")
        self.verticalLayout = QVBoxLayout(self.groupBox_info)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.groupBox_info)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.horizontalLayout_3.addWidget(self.groupBox_info)

        self.groupBox_setting = QGroupBox(self.centralwidget)
        self.groupBox_setting.setObjectName(u"groupBox_setting")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_setting)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox_setting)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.doubleSpinBox_global_wait_time = QDoubleSpinBox(self.groupBox_setting)
        self.doubleSpinBox_global_wait_time.setObjectName(u"doubleSpinBox_global_wait_time")
        self.doubleSpinBox_global_wait_time.setSingleStep(0.500000000000000)
        self.doubleSpinBox_global_wait_time.setValue(0.500000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBox_global_wait_time)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_setting)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox_loop_time = QSpinBox(self.groupBox_setting)
        self.spinBox_loop_time.setObjectName(u"spinBox_loop_time")
        self.spinBox_loop_time.setValue(1)

        self.horizontalLayout.addWidget(self.spinBox_loop_time)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_setting)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.spinBox_find_image_timeout = QSpinBox(self.groupBox_setting)
        self.spinBox_find_image_timeout.setObjectName(u"spinBox_find_image_timeout")
        self.spinBox_find_image_timeout.setMaximum(120)
        self.spinBox_find_image_timeout.setValue(30)

        self.horizontalLayout_5.addWidget(self.spinBox_find_image_timeout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_3.addWidget(self.groupBox_setting)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.groupBox_command = QGroupBox(self.centralwidget)
        self.groupBox_command.setObjectName(u"groupBox_command")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_command)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.groupBox_command)

        self.verticalLayout_5.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 877, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"waterRPA GUI\u7248", None))
        self.groupBox_config.setTitle(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e\u6587\u4ef6", None))
        self.toolButton_save_config.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.toolButton_add_config.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.toolButton_delete_config.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_function.setTitle(QCoreApplication.translate("MainWindow", u"\u6267\u884c\u533a", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.pushButton_listener.setText(QCoreApplication.translate("MainWindow", u"\u5f55\u5236", None))
        self.groupBox_info.setTitle(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>1.\u5168\u5c40\u8bbe\u7f6e-\u8fd0\u884c\u6b21\u6570\uff1a\u4e3a0\u65f6\uff0c\u4e3a\u65e0\u9650\u5faa\u73af\u3002</p><p>2.\u5168\u5c40\u8bbe\u7f6e-\u6307\u4ee4\u95f4\u9694\uff1a\u6bcf\u884c\u6307\u4ee4\u6267\u884c\u7684\u95f4\u9694\u65f6\u95f4\u3002</p><p>3.\u5168\u5c40\u8bbe\u7f6e-\u5bfb\u56fe\u8d85\u65f6\u65f6\u95f4\uff1a\u641c\u7d22\u6307\u5b9a\u56fe\u7247\u65f6\u7684\u8d85\u65f6\u65f6\u95f4\uff0c\u8d85\u8fc7\u5219\u7ec8\u6b62\u3002</p><p>4.\u9f20\u6807\u79fb\u81f3\u5c4f\u5e55\u6700\u5de6\u4e0a\u89d2\u65f6\uff0c\u53ef\u5f3a\u5236\u7ec8\u6b62\u8fd0\u884c\uff08\u8fd0\u884c\u7b49\u5f85\u6307\u4ee4\u65f6\u9664\u5916\uff09\u3002</p><p>5.\u5f55\u5236\u64cd\u4f5c\u540e\uff0c\u8bf7\u6ce8\u610f\u5168\u5c40\u8bbe\u7f6e-\u6307\u4ee4\u95f4\u9694\u3002</p></body></html>", None))
        self.groupBox_setting.setTitle(QCoreApplication.translate("MainWindow", u"\u5168\u5c40\u8bbe\u7f6e", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6307\u4ee4\u95f4\u9694/\u79d2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u6b21\u6570", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5bfb\u56fe\u8d85\u65f6\u65f6\u95f4/\u79d2", None))
        self.groupBox_command.setTitle(QCoreApplication.translate("MainWindow", u"\u6307\u4ee4\u533a", None))
    # retranslateUi

