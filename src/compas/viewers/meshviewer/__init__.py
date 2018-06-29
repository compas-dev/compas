from .view import View
from .controller import Controller

import os

here = os.path.abspath(os.path.dirname(__file__))

CONFIG = {
    'menubar': [
        {
            'type'  : 'menu',
            'text'  : 'View',
            'items' : [
                {
                    'type'  : 'menu',
                    'text'  : 'Set View',
                    'items' : [
                        {
                            'type'  : 'radio',
                            'items' : [
                                {
                                    'text'    : 'Perspective',
                                    'action'  : 'set_view',
                                    'args'    : [View.VIEW_PERSPECTIVE, ],
                                    'checked' : True
                                },
                                {
                                    'text'    : 'Front',
                                    'action'  : 'set_view',
                                    'args'    : [View.VIEW_FRONT, ],
                                    'checked' : False
                                },
                                {
                                    'text'    : 'Left',
                                    'action'  : 'set_view',
                                    'args'    : [View.VIEW_LEFT, ],
                                    'checked' : False
                                },
                                {
                                    'text'    : 'Top',
                                    'action'  : 'set_view',
                                    'args'    : [View.VIEW_TOP, ],
                                    'checked' : False
                                },
                            ]
                        }
                    ]
                },
                {'type' : 'separator'},
                {'text' : 'Camera', 'action': 'update_camera_settings'},
                {'type' : 'separator'},
                {'text' : 'Capture Image', 'action': 'capture_image'},
                {'text' : 'Capture Video', 'action': 'capture_video'},
                {'type' : 'separator'}
            ]
        },
        {
            'type'  : 'menu',
            'text'  : 'Mesh',
            'items' : [
                {'text' : 'From OBJ', 'action': 'from_obj'},
                {'text' : 'From JSON', 'action': 'from_json'},
                {'text' : 'From STL', 'action': 'from_stl'},
                {'text' : 'From PLY', 'action': 'from_ply'},
                {'type' : 'separator'},
                {'text' : 'To OBJ', 'action': 'to_obj'},
                {'text' : 'To JSON', 'action': 'to_json'},
                {'text' : 'To STL', 'action': 'to_stl'},
                {'text' : 'To PLY', 'action': 'to_ply'},
                {'type' : 'separator'},
                {
                    'type' : 'menu',
                    'text' : 'Polyhedrons',
                    'items': [
                        {'text': 'Tetrahedron', 'action': 'from_polyhedron', 'args': [4]},
                        {'text': 'Hexahedron', 'action': 'from_polyhedron', 'args': [6]},
                        {'text': 'Octahedron', 'action': 'from_polyhedron', 'args': [8]},
                        {'text': 'Dodecahedron', 'action': 'from_polyhedron', 'args': [12]},
                    ]
                },
                {'type' : 'separator'},
            ]
        },
        {
            'type'  : 'menu',
            'text'  : 'Tools',
            'items' : [
                {'text': 'Flip Normals', 'action': 'flip_normals'},
                {'type': 'separator'},
                {
                    'type'  : 'menu',
                    'text'  : 'Subdivision',
                    'items' : [
                        {'text': 'Catmull-Clark', 'action': 'subdivide', 'args': ['catmullclark', 1]}
                    ]
                }
            ]
        },
        {
            'type'  : 'menu',
            'text'  : 'OpenGL',
            'items' : [
                {'text' : 'Version Info', 'action': 'opengl_version_info'},
                {'type' : 'separator'},
                {
                    'type'  : 'radio',
                    'items' : [
                        {
                            'text'    : 'Version 2.1',
                            'action'  : 'opengl_set_version',
                            'args'    : [(2, 1), ],
                            'checked' : True
                        },
                        {
                            'text'    : 'Version 3.3',
                            'action'  : 'opengl_set_version',
                            'args'    : [(3, 3), ],
                            'checked' : False
                        },
                        {
                            'text'    : 'Version 4.1',
                            'action'  : 'opengl_set_version',
                            'args'    : [(4, 1), ],
                            'checked' : False
                        }
                    ]
                },
            ]
        },
        {
            'type'  : 'menu',
            'text'  : 'Window',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Help',
            'items' : []
        }
    ],
    'toolbar': [
        {'text': 'Zoom Extents', 'action': 'zoom_extents', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-to-extents-50.png')},
        {'text': 'Zoom In', 'action': 'zoom_in', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-in-50.png')},
        {'text': 'Zoom Out', 'action': 'zoom_out', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-out-50.png')},
    ],
    'sidebar': [
        {
            'type'  : 'group',
            'text'  : None,
            'items' : [
                {
                    'type'  : 'group',
                    'text'  : None,
                    'items' : [
                        {'type' : 'checkbox', 'text' : 'vertices', 'action' : 'toggle_vertices', 'state' : True, },
                        {'type' : 'checkbox', 'text' : 'edges', 'action' : 'toggle_edges', 'state' : True, },
                        {'type' : 'checkbox', 'text' : 'faces', 'action' : 'toggle_faces', 'state' : True, },
                    ]
                },
                {
                    'type'  : 'group',
                    'text'  : None,
                    'items' : [
                        {'type' : 'checkbox', 'text' : 'normals', 'action' : 'toggle_normals', 'state' : False, },
                    ]
                },
            ]
        },
        {
            'type' : 'group',
            'text' : None,
            'items': [
                {
                    'type' : 'group',
                    'text' : None,
                    'items': [
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color vertices',
                            'value' : Controller.settings['vertices.color'],
                            'action': 'change_vertices_color',
                        },
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color edges',
                            'value' : Controller.settings['edges.color'],
                            'action': 'change_edges_color',
                        },
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color faces (front)',
                            'value' : Controller.settings['faces.color:front'],
                            'action': 'change_faces_color_front',
                        },
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color faces (back)',
                            'value' : Controller.settings['faces.color:back'],
                            'action': 'change_faces_color_back',
                        },
                    ]
                },
                {
                    'type' : 'group',
                    'text' : None,
                    'items': [
                        {
                            'type'   : 'slider',
                            'text'   : 'size vertices',
                            'value'  : Controller.settings['vertices.size:value'],
                            'minval' : Controller.settings['vertices.size:minval'],
                            'maxval' : Controller.settings['vertices.size:maxval'],
                            'step'   : Controller.settings['vertices.size:step'],
                            'scale'  : Controller.settings['vertices.size:scale'],
                            'slide'  : 'slide_size_vertices',
                            'edit'   : 'edit_size_vertices',
                        },
                        {
                            'type'   : 'slider',
                            'text'   : 'width edges',
                            'value'  : Controller.settings['edges.width:value'],
                            'minval' : Controller.settings['edges.width:minval'],
                            'maxval' : Controller.settings['edges.width:maxval'],
                            'step'   : Controller.settings['edges.width:step'],
                            'scale'  : Controller.settings['edges.width:scale'],
                            'slide'  : 'slide_width_edges',
                            'edit'   : 'edit_width_edges',
                        }
                    ]
                }
            ]
        }
    ]
}

STYLE = """
QMainWindow {}

QMenuBar {}

QToolBar#Tools {
padding: 4px;
}

QDockWidget#Sidebar {}

QDockWidget#Console {}

QDockWidget#Console QPlainTextEdit {
background-color: #222222;
color: #eeeeee;
border-top: 8px solid #cccccc;
border-left: 1px solid #cccccc;
border-right: 1px solid #cccccc;
border-bottom: 1px solid #cccccc;
padding-left: 4px;
}
"""

from .app import MeshViewer


__all__ = ['MeshViewer', ]

