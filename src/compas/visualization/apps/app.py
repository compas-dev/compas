from __future__ import print_function

import sys

from PySide.QtCore import Qt

from PySide.QtGui import QMainWindow
from PySide.QtGui import QApplication
from PySide.QtGui import QDockWidget
from PySide.QtGui import QWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['App', ]


class App(QApplication):
    """"""

    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setApplicationName("Viewer app")
        self.setup()
        self.main.setFixedSize(1264, 768)
        self.main.show()

    def setup(self):
        self.setup_mainwindow()

    def start(self):
        sys.exit(self.exec_())

    def setup_mainwindow(self):
        self.main = QMainWindow()
        self.setup_centralwidget()
        self.setup_menubar()
        self.setup_sidebar()
        self.setup_statusbar()

    def setup_centralwidget(self):
        self.view = view = View(self)
        view.setFocusPolicy(Qt.StrongFocus)
        view.setFocus()
        self.main.setCentralWidget(view)

    def setup_menubar(self):
        self.menu = menu = self.main.menuBar()
        self.main.setMenuBar(menu)
        self.add_filemenu()

    def add_filemenu(self):
        menu = self.menu.addMenu('&File')
        new_action = menu.addAction('&New')
        new_action.triggered.connect(self.do_newfile)

    def do_newfile(self):
        print('i am doing it!')

    def setup_sidebar(self):
        self.sidebar = sidebar = QDockWidget()
        sidebar.setAllowedAreas(Qt.LeftDockWidgetArea)
        sidebar.setFeatures(QDockWidget.NoDockWidgetFeatures)
        sidebar.setFixedWidth(240)
        widget = QWidget(sidebar)
        # add stuff here
        # provide a callback?
        sidebar.setWidget(widget)
        print(sidebar.size())
        self.main.addDockWidget(Qt.LeftDockWidgetArea, sidebar)

    def setup_statusbar(self):
        self.status = self.main.statusBar()
        self.main.setStatusBar(self.status)
        self.status.showMessage('status')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
