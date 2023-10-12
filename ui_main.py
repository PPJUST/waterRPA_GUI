# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_maincVdiot.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(683, 501)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.groupBox_instruct = QGroupBox(self.centralwidget)
        self.groupBox_instruct.setObjectName(u"groupBox_instruct")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_instruct)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget_instruct_area = QListWidget(self.groupBox_instruct)
        self.listWidget_instruct_area.setObjectName(u"listWidget_instruct_area")

        self.verticalLayout_2.addWidget(self.listWidget_instruct_area)


        self.horizontalLayout_3.addWidget(self.groupBox_instruct)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_config = QGroupBox(self.centralwidget)
        self.groupBox_config.setObjectName(u"groupBox_config")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_config)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.comboBox_select_config = QComboBox(self.groupBox_config)
        self.comboBox_select_config.setObjectName(u"comboBox_select_config")

        self.horizontalLayout_2.addWidget(self.comboBox_select_config)

        self.toolButton_add_config = QToolButton(self.groupBox_config)
        self.toolButton_add_config.setObjectName(u"toolButton_add_config")

        self.horizontalLayout_2.addWidget(self.toolButton_add_config)

        self.toolButton_delete_config = QToolButton(self.groupBox_config)
        self.toolButton_delete_config.setObjectName(u"toolButton_delete_config")

        self.horizontalLayout_2.addWidget(self.toolButton_delete_config)


        self.verticalLayout_3.addWidget(self.groupBox_config)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.groupBox_function = QGroupBox(self.centralwidget)
        self.groupBox_function.setObjectName(u"groupBox_function")
        self.gridLayout = QGridLayout(self.groupBox_function)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_function)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox_loop_time = QSpinBox(self.groupBox_function)
        self.spinBox_loop_time.setObjectName(u"spinBox_loop_time")
        self.spinBox_loop_time.setValue(1)

        self.horizontalLayout.addWidget(self.spinBox_loop_time)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.pushButton_start = QPushButton(self.groupBox_function)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.gridLayout.addWidget(self.pushButton_start, 0, 0, 1, 1)

        self.pushButton_stop = QPushButton(self.groupBox_function)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.gridLayout.addWidget(self.pushButton_stop, 0, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_function)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.groupBox_info = QGroupBox(self.centralwidget)
        self.groupBox_info.setObjectName(u"groupBox_info")
        self.verticalLayout = QVBoxLayout(self.groupBox_info)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.groupBox_info)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.verticalLayout_3.addWidget(self.groupBox_info)

        self.verticalLayout_3.setStretch(4, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 683, 23))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"waterRPA GUI\u7248", None))
        self.groupBox_instruct.setTitle(QCoreApplication.translate("MainWindow", u"\u6307\u4ee4\u533a", None))
        self.groupBox_config.setTitle(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e\u6587\u4ef6", None))
        self.toolButton_add_config.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.toolButton_delete_config.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_function.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd\u533a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u6b21\u6570", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.groupBox_info.setTitle(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7b80\u5355\u8bf4\u660e", None))
    # retranslateUi

