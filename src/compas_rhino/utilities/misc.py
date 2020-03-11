from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys
import ast

import compas

from compas_rhino.forms import TextForm
from compas_rhino.forms import ImageForm

try:
    basestring
except NameError:
    basestring = str

try:
    import rhinoscriptsyntax as rs
    import System
    import Rhino

except ImportError:
    compas.raise_if_ironpython()

# check if MessageBox is already available for Mac
try:
    from Rhino.UI.Dialogs import ShowMessageBox

except ImportError:
    compas.raise_if_ironpython()

# replace PropertyListBox by Eto form on Mac and Rhino 6
try:
    from compas_rhino.etoforms import PropertyListForm

except Exception:
    try:
        from Rhino.UI.Dialogs import ShowPropertyListBox

    except ImportError:
        compas.raise_if_ironpython()
else:
    try:
        import clr
        clr.AddReference('Rhino.UI')
        import Rhino.UI

    except ImportError:
        compas.raise_if_ironpython()


__all__ = [
    'wait',
    'get_tolerance',
    'toggle_toolbargroup',
    'pick_point',
    'browse_for_folder',
    'browse_for_file',
    'print_display_on',
    'display_message',
    'display_text',
    'display_image',
    'display_html',
    'update_settings',
    'update_named_values',
    'screenshot_current_view',
    'select_folder',
    'select_file',
    'unload_modules',
]


# ==============================================================================
# Truly miscellaneous :)
# ==============================================================================


def screenshot_current_view(path,
                            width=1920,
                            height=1080,
                            scale=1,
                            draw_grid=False,
                            draw_world_axes=False,
                            draw_cplane_axes=False,
                            background=False):
    properties = [draw_grid, draw_world_axes, draw_cplane_axes, background]
    properties = ["Yes" if item else "No" for item in properties]
    scale = max(1, scale)  # the rhino command requires a scale > 1
    rs.EnableRedraw(True)
    rs.Sleep(0)
    result = rs.Command("-_ViewCaptureToFile \"" + os.path.abspath(path) + "\""
                        " Width=" + str(width) +
                        " Height=" + str(height) +
                        " Scale=" + str(scale) +
                        " DrawGrid=" + properties[0] +
                        " DrawWorldAxes=" + properties[1] +
                        " DrawCPlaneAxes=" + properties[2] +
                        " TransparentBackground=" + properties[3] +
                        " _enter", False)
    rs.EnableRedraw(False)
    return result


def wait():
    return Rhino.RhinoApp.Wait()


def get_tolerance():
    return rs.UnitAbsoluteTolerance()


def toggle_toolbargroup(rui, group):
    if not os.path.exists(rui) or not os.path.isfile(rui):
        return
    collection = rs.IsToolbarCollection(rui)
    if not collection:
        collection = rs.OpenToolbarCollection(rui)
        if rs.IsToolbar(collection, group, True):
            rs.ShowToolbar(collection, group)
    else:
        if rs.IsToolbar(collection, group, True):
            if rs.IsToolbarVisible(collection, group):
                rs.HideToolbar(collection, group)
            else:
                rs.ShowToolbar(collection, group)


# pick a location
# get_location
def pick_point(message='Pick a point.'):
    point = rs.GetPoint(message)
    if point:
        return list(point)
    return None


# ==============================================================================
# File system
# ==============================================================================


def browse_for_folder(message=None, default=None):
    return rs.BrowseForFolder(folder=default, message=message, title='compas')


select_folder = browse_for_folder


def browse_for_file(title=None, folder=None, filter=None):
    if filter == 'json':
        filter = 'JSON files (*.json)|*.json||'
    elif filter == 'obj':
        filter = 'OBJ files (*.obj)|*.obj||'
    elif filter == 'fofin':
        filter = 'FOFIN session files (*.fofin)|*.fofin||'
    else:
        pass
    return rs.OpenFileName(title, filter=filter, folder=folder)


select_file = browse_for_file


# ==============================================================================
# Display
# ==============================================================================


def print_display_on(on=True):
    if on:
        rs.Command('_PrintDisplay State On Color Display Thickness 1 _Enter')
    else:
        rs.Command('_PrintDisplay State Off _Enter')


def display_message(message):
    return ShowMessageBox(message, 'Message')


def display_text(text, title='Text', width=800, height=600):
    if isinstance(text, (list, tuple)):
        text = '{0}'.format(System.Environment.NewLine).join(text)
    form = TextForm(text, title, width, height)
    return form.show()


def display_image(image, title='Image', width=800, height=600):
    form = ImageForm(image, title, width, height)
    return form.show()


def display_html():
    raise NotImplementedError


# ==============================================================================
# Settings and attributes
# ==============================================================================


def update_named_values(names, values, message='', title='Update named values', evaluate=False):
    try:
        dialog = PropertyListForm(names, values)
    except Exception:
        values = ShowPropertyListBox(message, title, names, values)
    else:
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None
    if evaluate:
        if values:
            values = list(values)
            for i in range(len(values)):
                value = values[i]
                try:
                    value = ast.literal_eval(value)
                except (TypeError, ValueError, SyntaxError):
                    pass
                values[i] = value
    return values


def update_settings(settings, message='', title='Update settings'):
    names = sorted(settings.keys())
    values = [str(settings[name]) for name in names]
    values = update_named_values(names, values, message=message, title=title)
    if values:
        values = list(values)
        for name, value in zip(names, values):
            try:
                settings[name] = ast.literal_eval(value)
            except (TypeError, ValueError, SyntaxError):
                settings[name] = value
        return True
    return False


def unload_modules(top_level_module_name):
    """Unloads all modules named starting with the specified string.

    This function eases the development workflow when editing a library that is
    used from Rhino/Grasshopper.

    Args:
        top_level_module_name (:obj:`str`): Name of the top-level module to unload.

    Returns:
        list: List of unloaded module names.
    """
    modules = filter(lambda m: m.startswith(top_level_module_name), sys.modules)

    for module in modules:
        sys.modules.pop(module)

    return modules


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
