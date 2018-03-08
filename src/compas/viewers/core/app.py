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

    def __init__(self, config, style):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.config = config or {}
        self.style = style or """"""
        self.setApplicationName("Viewer app")
        self.setStyleSheet(self.style)

    def setup(self, w, h):
        self.main = QtWidgets.QMainWindow()
        self.main.setFixedSize(w, h)
        self.main.setGeometry(0, 0, w, h)
        self.main.setCentralWidget(self.view)

    def init(self):
        self.init_menubar()
        self.init_toolbar()
        self.init_sidebar()
        self.init_statusbar()
        self.init_console()

    def show(self):
        self.main.show()
        self.main.raise_()
        self.start()

    def start(self):
        sys.exit(self.exec_())

    def init_statusbar(self):
        self.statusbar = self.main.statusBar()
        self.statusbar.showMessage('Ready')

    def init_menubar(self):
        if 'menubar' not in self.config:
            return
        self.menubar = self.main.menuBar()
        self.add_menubar_items(self.config['menubar'], self.menubar, 0)

    def init_toolbar(self):
        if 'toolbar' not in self.config:
            return
        self.toolbar = self.main.addToolBar('Tools')
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName('Tools')
        self.toolbar.setIconSize(QtCore.QSize(24, 24))
        self.add_toolbar_items(self.config['toolbar'], self.toolbar)

    def init_sidebar(self):
        if 'sidebar' not in self.config:
            return
        self.sidebar = QtWidgets.QDockWidget()
        self.sidebar.setObjectName('Sidebar')
        self.sidebar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.sidebar.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.sidebar.setFixedWidth(240)
        self.sidebar.setTitleBarWidget(QtWidgets.QWidget())
        self.main.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.sidebar)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(4, 8, 4, 8)
        widget.setLayout(layout)
        self.sidebar.setWidget(widget)
        self.add_sidebar_items(self.config['sidebar'], layout)
        layout.addStretch()

    def init_console(self):
        self.console = QtWidgets.QDockWidget()
        self.console.setObjectName('Console')
        self.console.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.console.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.console.setFixedHeight(128)
        self.console.setTitleBarWidget(QtWidgets.QWidget())
        self.main.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.console)
        editor = QtWidgets.QPlainTextEdit()
        editor.setReadOnly(True)
        self.console.setWidget(editor)

    # ==========================================================================
    # add multiple
    # ==========================================================================

    def add_menubar_items(self, items, parent, level):
        if not items:
            return
        for item in items:
            itype = item.get('type', None)
            if itype == 'separator':
                parent.addSeparator()
                continue
            if itype == 'menu':
                menu = parent.addMenu(item['text'])
                if 'items' in item:
                    self.add_menubar_items(item['items'], menu, level + 1)
                continue
            if itype == 'radio':
                radio = QtWidgets.QActionGroup(self.main, exclusive=True)
                for item in item['items']:
                    action = self.add_action(item, parent)
                    action.setCheckable(True)
                    action.setChecked(item['checked'])
                    radio.addAction(action)
                continue
            self.add_action(item, parent)

    def add_toolbar_items(self, items, parent):
        if not items:
            return
        for item in items:
            itype = item.get('type', None)
            if itype == 'separator':
                parent.addSeparator()
                continue
            self.add_action(item, parent)

    def add_sidebar_items(self, items, parent):
        if not items:
            return
        for item in items:
            itype = item.get('type', None)
            if itype == 'group':
                self.add_group(item, parent)
                continue
            if itype == 'checkbox':
                self.add_checkbox(item, parent)
                continue
            if itype == 'slider':
                self.add_slider(item, parent)
                continue
            if itype == 'button':
                self.add_button(item, parent)
                continue
            if itype == 'colorbutton':
                self.add_colorbutton(item, parent)
                continue

    # ==========================================================================
    # add one
    # ==========================================================================

    def add_action(self, item, parent):
        text = item['text']
        if hasattr(self.controller, item['action']):
            action = getattr(self.controller, item['action'])
            args = item.get('args', None) or []
            kwargs = item.get('kwargs', None) or {}
            if 'image' in item:
                icon = QtWidgets.QIcon(item['image'])
                return parent.addAction(icon, text, partial(action, *args, **kwargs))
            return parent.addAction(text, partial(action, *args, **kwargs))
        if 'image' in item:
            icon = QtWidgets.QIcon(item['image'])
            return parent.addAction(icon, text)
        return parent.addAction(text)

    def add_group(self, item, parent):
        group = QtWidgets.QGroupBox(item.get('text', None))
        box = QtWidgets.QVBoxLayout()
        box.setContentsMargins(0, 4, 0, 4)
        group.setLayout(box)
        parent.addWidget(group)
        self.add_sidebar_items(item['items'], box)

    def add_slider(self, item, parent):
        slider = Slider(item['text'],
                        item['value'],
                        item['minval'],
                        item['maxval'],
                        item['step'],
                        item['scale'],
                        getattr(self.controller, item['slide']),
                        getattr(self.controller, item['edit']))
        parent.addLayout(slider.layout)

    def add_checkbox(self, item, parent):
        checkbox = QtWidgets.QCheckBox(item['text'])
        checkbox.setCheckState(QtCore.Qt.Checked if item['state'] else QtCore.Qt.Unchecked)
        if item['action']:
            checkbox.stateChanged.connect(getattr(self.controller, item['action']))
        parent.addWidget(checkbox)

    def add_button(self, item, parent):
        pass

    def add_colorbutton(self, item, parent):
        button = ColorButton(item['text'],
                             color=item['value'],
                             size=item.get('size'),
                             action=getattr(self.controller, item.get('action')))
        parent.addLayout(button.layout)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
