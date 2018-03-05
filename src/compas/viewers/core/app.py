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

from compas.viewers.core import ColorButton
from compas.viewers.core import Slider


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

    def setup(self, w, h):
        self.main = QtWidgets.QMainWindow()
        self.main.setFixedSize(w, h)
        self.main.setGeometry(0, 0, w, h)
        self.main.setCentralWidget(self.view)
        self.statusbar = self.main.statusBar()

    def init(self):
        if self.config:
            if 'menubar' in self.config:
                self.init_menubar()
            if 'toolbar' in self.config:
                self.init_toolbar()
            if 'sidebar' in self.config:
                self.init_sidebar()

    def show(self):
        self.statusbar.showMessage('Ready')
        self.main.show()
        self.main.raise_()
        self.start()

    def start(self):
        sys.exit(self.exec_())

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

    def init_sidebar(self):
        def make_items(items, parent):
            for item in items:
                itype = item.get('type', None)
                if itype == 'group':
                    make_group(item, parent)
                    continue
                if itype == 'checkbox':
                    make_checkbox(item, parent)
                    continue
                if itype == 'slider':
                    make_slider(item, parent)
                    continue
                if itype == 'button':
                    make_slider(item, parent)
                    continue
                if itype == 'colorbutton':
                    make_colorbutton(item, parent)
                    continue

        def make_group(item, parent):
            group = QtWidgets.QGroupBox(item.get('text', None))
            box = QtWidgets.QVBoxLayout()
            group.setLayout(box)
            make_items(item.get('items'), box)
            parent.addWidget(group)

        def make_slider(item, parent):
            slider = Slider(item['text'],
                            item['value'],
                            item['minval'],
                            item['maxval'],
                            item['step'],
                            item['scale'],
                            getattr(self.controller, item['slide']),
                            getattr(self.controller, item['edit']))
            parent.addLayout(slider.layout)

        def make_checkbox(item, parent):
            checkbox = QtWidgets.QCheckBox(item['text'])
            checkbox.setCheckState(QtCore.Qt.Checked if item['state'] else QtCore.Qt.Unchecked)
            if item['action']:
                checkbox.stateChanged.connect(item['action'])
            parent.addWidget(checkbox)

        def make_button(item, parent):
            pass

        def make_colorbutton(item, parent):
            button = ColorButton(item['text'],
                                 color=item['value'],
                                 size=item.get('size'),
                                 action=item.get('action'))
            parent.addLayout(button.layout)

        self.sidebar = QtWidgets.QDockWidget('Sidebar')
        self.sidebar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.sidebar.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.sidebar.setFixedWidth(240)
        self.main.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.sidebar)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        self.sidebar.setWidget(widget)

        make_items(self.config['sidebar'], layout)

        layout.addStretch()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
