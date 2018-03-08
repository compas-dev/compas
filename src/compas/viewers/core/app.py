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


# menubar, sidebar, toolbar as separate classes!


class App(QtWidgets.QApplication):
    """"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.setApplicationName("Viewer app")
#         self.setStyleSheet("""
# QVBoxLayout {
#     padding: 4px;
# }
# """)

    def setup(self, w, h):
        self.main = QtWidgets.QMainWindow()
        self.main.setFixedSize(w, h)
        self.main.setGeometry(0, 0, w, h)
        self.main.setCentralWidget(self.view)
        self.statusbar = self.main.statusBar()
        self.console = QtWidgets.QDockWidget()
        self.console

    def init(self):
        if self.config:
            if 'menubar' in self.config:
                self.init_menubar()
            if 'toolbar' in self.config:
                self.init_toolbar()
            if 'sidebar' in self.config:
                self.init_sidebar()
        self.init_console()

    def show(self):
        self.statusbar.showMessage('Ready')
        self.main.show()
        self.main.raise_()
        self.start()

    def start(self):
        sys.exit(self.exec_())

    # this can be a lot simpler
    # see, for example, init_toolbar
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
                if mtype == 'radio':
                    radio = QtWidgets.QActionGroup(self.main, exclusive=True)
                    for item in item['items']:
                        action = parent.addAction(item['text'])
                        action.setCheckable(True)
                        action.setChecked(item['checked'])
                        handler = item.get('action', None)
                        if handler:
                            if hasattr(self.controller, handler):
                                handler = getattr(self.controller, handler)
                                args = item.get('args', [])
                                kwargs = item.get('kwargs', {})
                                if args or kwargs:
                                    handler = partial(handler, *args, **kwargs)
                                action.triggered.connect(handler)
                        radio.addAction(action)
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
        self.toolbar.setStyleSheet("""
QToolBar {
    padding: 4px;
}
""")
        self.toolbar.setIconSize(QtCore.QSize(24, 24))
        for item in self.config['toolbar']:
            itype = item.get('type', None)
            if itype == 'separator':
                self.toolbar.addSeparator()
                continue
            text = item['text']
            if 'image' in item:
                icon = QtWidgets.QIcon(item['image'])
                if item['action']:
                    action = getattr(self.controller, item['action'])
                    self.toolbar.addAction(icon, text, action)
                else:
                    self.toolbar.addAction(icon, text)
            else:
                if item['action']:
                    action = getattr(self.controller, item['action'])
                    self.toolbar.addAction(text, action)
                else:
                    self.toolbar.addAction(text)

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
            # box.setSpacing(0)
            box.setContentsMargins(0, 4, 0, 4)
            group.setLayout(box)
#             group.setStyleSheet("""
# background: none;
# border: none;
# border-bottom: 1px solid #ffffff;
# """)
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
                checkbox.stateChanged.connect(getattr(self.controller, item['action']))
            parent.addWidget(checkbox)

        def make_button(item, parent):
            pass

        def make_colorbutton(item, parent):
            button = ColorButton(item['text'],
                                 color=item['value'],
                                 size=item.get('size'),
                                 action=getattr(self.controller, item.get('action')))
            parent.addLayout(button.layout)

        self.sidebar = QtWidgets.QDockWidget('Sidebar')
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

        make_items(self.config['sidebar'], layout)

        layout.addStretch()

    def init_console(self):
        dock = QtWidgets.QDockWidget('Console')
        dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        # dock.setMaximumHeight(320)
        # dock.setMinimumHeight(32)
        # dock.setHeight(32)
        dock.setFixedHeight(128)
        dock.setTitleBarWidget(QtWidgets.QWidget())

        self.main.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)

        self.console = QtWidgets.QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
QPlainTextEdit {
    background-color: #222222;
    color: #eeeeee;
    border-top: 8px solid #cccccc;
    border-left: 1px solid #cccccc;
    border-right: 1px solid #cccccc;
    border-bottom: 1px solid #cccccc;
    padding-left: 4px;
}
""")

        for i in range(1):
            self.console.appendPlainText('Stuff man, stuff...')

        dock.setWidget(self.console)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
