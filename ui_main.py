# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainBZLeqC.ui'
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
        MainWindow.resize(748, 699)
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
        self.pushButton_start.setEnabled(False)

        self.gridLayout.addWidget(self.pushButton_start, 0, 0, 1, 1)

        self.pushButton_stop = QPushButton(self.groupBox_function)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setEnabled(False)

        self.gridLayout.addWidget(self.pushButton_stop, 0, 1, 1, 1)


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

        self.horizontalLayout_3.addWidget(self.groupBox_setting)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.groupBox_instruct = QGroupBox(self.centralwidget)
        self.groupBox_instruct.setObjectName(u"groupBox_instruct")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_instruct)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget_instruct_area = QListWidget(self.groupBox_instruct)
        self.listWidget_instruct_area.setObjectName(u"listWidget_instruct_area")

        self.verticalLayout_2.addWidget(self.listWidget_instruct_area)


        self.verticalLayout_5.addWidget(self.groupBox_instruct)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 748, 23))
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
        self.groupBox_function.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u6b21\u6570", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.groupBox_info.setTitle(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7b80\u5355\u8bf4\u660e", None))
        self.groupBox_setting.setTitle(QCoreApplication.translate("MainWindow", u"\u5168\u5c40\u8bbe\u7f6e", None))
        self.groupBox_instruct.setTitle(QCoreApplication.translate("MainWindow", u"\u6307\u4ee4\u533a", None))
    # retranslateUi

