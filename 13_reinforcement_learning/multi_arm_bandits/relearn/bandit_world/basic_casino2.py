# -*- coding: utf-8 -*-

"""
Module implementing MainWindow2.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from .Ui_basic_casino2 import Ui_MainWindow


class MainWindow2(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow2, self).__init__(parent)
        self.setupUi(self)
