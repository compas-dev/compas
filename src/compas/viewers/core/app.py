from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys

from functools import partial

try:
    import PySide2
except ImportError:
    from PySide import QtCore
    from PySide import QtGui
    import PySide.QtGui as QtWidgets
else:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['App', ]


class App(QtWidgets.QApplication):
    """"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.setApplicationName("Viewer app")

    def start(self):
        sys.exit(self.exec_())

    def show(self):
        self.statusbar.showMessage('Ready')
        self.main.show()
        self.main.raise_()
        self.start()

    def setup(self, w, h):
        self.main = QtWidgets.QMainWindow()
        self.main.setFixedSize(w, h)
        self.main.setGeometry(0, 0, w, h)
        self.main.setCentralWidget(self.view)

    def init(self):
        self.init_statusbar()
        if not self.config:
            return
        if 'menubar' in self.config:
            self.init_menubar()
        if 'toolbar' in self.config:
            self.init_toolbar()
        if 'panel' in self.config:
            self.init_panel()

    def init_statusbar(self):
        self.statusbar = self.main.statusBar()

    def init_menubar(self):
        def make_menu(menu, parent):
            for item in menu:
                mtype = item.get('type', None)
                if mtype == 'separator':
                    parent.addSeparator()
                    continue
                if mtype == 'menu':
                    newmenu = parent.addMenu(item['text'])
                    items = item.get('items')
                    if items:
                        make_menu(items, newmenu)
                    continue
                action = parent.addAction(item['text'])
                handler = item.get('action', None)
                if handler:
                    if hasattr(self.controller, handler):
                        handler = getattr(self.controller, handler)
                        args = item.get('args', [])
                        kwargs = item.get('kwargs', {})
                        if args or kwargs:
                            handler = partial(handler, *args, **kwargs)
                        action.triggered.connect(handler)
        self.menubar = self.main.menuBar()
        make_menu(self.config['menubar'], self.menubar)

    def init_toolbar(self):
        self.toolbar = self.main.addToolBar('Tools')
        self.toolbar.setMovable(False)

    def init_panel(self):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
