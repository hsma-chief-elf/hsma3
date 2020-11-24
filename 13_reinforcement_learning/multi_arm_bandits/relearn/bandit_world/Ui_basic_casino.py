# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Dropbox/Python/multi-arm-bandit/relearn/bandit_world/basic_casino.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
import random 

import matplotlib.pyplot as plt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 399)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 231, 80))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lbl_pull_count = QtWidgets.QLCDNumber(self.formLayoutWidget_2)
        self.lbl_pull_count.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lbl_pull_count.setProperty("value", 0.0)
        self.lbl_pull_count.setProperty("intValue", 0)
        self.lbl_pull_count.setObjectName("lbl_pull_count")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lbl_pull_count)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lbl_pull_count_2 = QtWidgets.QLCDNumber(self.formLayoutWidget_2)
        self.lbl_pull_count_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lbl_pull_count_2.setProperty("value", 0.0)
        self.lbl_pull_count_2.setProperty("intValue", 0)
        self.lbl_pull_count_2.setObjectName("lbl_pull_count_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lbl_pull_count_2)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 188, 231))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.verticalLayoutWidget.setFont(font)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pull_arm1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pull_arm1.setFont(font)
        self.pull_arm1.setObjectName("pull_arm1")
        self.verticalLayout.addWidget(self.pull_arm1)
        self.pull_arm2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pull_arm2.setFont(font)
        self.pull_arm2.setObjectName("pull_arm2")
        self.verticalLayout.addWidget(self.pull_arm2)
        self.pull_arm3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pull_arm3.setFont(font)
        self.pull_arm3.setObjectName("pull_arm3")
        self.verticalLayout.addWidget(self.pull_arm3)
        self.pull_arm4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pull_arm4.setFont(font)
        self.pull_arm4.setObjectName("pull_arm4")
        self.verticalLayout.addWidget(self.pull_arm4)
        self.pull_arm4_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pull_arm4_2.setFont(font)
        self.pull_arm4_2.setObjectName("pull_arm4_2")
        self.verticalLayout.addWidget(self.pull_arm4_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(250, 10, 481, 321))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 461, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.tableWidget.setFont(font)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(55)
        self.pull_arm4_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pull_arm4_3.setGeometry(QtCore.QRect(10, 340, 186, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pull_arm4_3.setFont(font)
        self.pull_arm4_3.setObjectName("pull_arm4_3")
        #here...
        #self.add_plot()

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bandit Casino "))
        self.label.setText(_translate("MainWindow", "Rounds"))
        self.label_2.setText(_translate("MainWindow", "Reward"))
        self.pull_arm1.setText(_translate("MainWindow", "Play Bandit 1"))
        self.pull_arm2.setText(_translate("MainWindow", "Play Bandit 2"))
        self.pull_arm3.setText(_translate("MainWindow", "Play Bandit 3"))
        self.pull_arm4.setText(_translate("MainWindow", "Play Bandit 4"))
        self.pull_arm4_2.setText(_translate("MainWindow", "Play Bandit 5"))
        self.groupBox.setTitle(_translate("MainWindow", "State"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Bandit 1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Bandit 2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Bandit 3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Bandit 4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Bandit 5"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Pulls"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Wins"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Win %"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pull_arm4_3.setText(_translate("MainWindow", "Reset"))

    def add_plot(self):

        # a figure instance to plot on
        self.figure = plt.figure()
        
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        #layout = QVBoxLayout(self.centralWidget)
        #layout.setGeometry(QtCore.QRect(500, 340, 186, 41))
        #self.pull_arm4_3.setGeometry(QtCore.QRect(10, 340, 186, 41))
        
        layout = QtWidgets.QGridLayout(self.centralWidget)
        layout.setGeometry(QtCore.QRect(10, 10, 10, 10))
    
        #layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        #self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]
        x = [i + 1 for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        
        #ax.plot(data, '*-')
        ax.bar(x, data)

        # refresh canvas
        self.canvas.draw()

#handler for the signal aka slot
def onClick():
    print('clicked')
    





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.pull_arm1.clicked.connect(onClick)
    print(ui.tableWidget.item(0, 0))
    MainWindow.show()
    sys.exit(app.exec_())

