from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import rhinoscriptsyntax as rs  # type: ignore


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


def pick_point(message="Pick a point."):
    point = rs.GetPoint(message)
    if point:
        return list(point)
    return None


def browse_for_folder(message=None, default=None):
    return rs.BrowseForFolder(folder=default, message=message, title="compas")


select_folder = browse_for_folder


def browse_for_file(title=None, folder=None, filter=None):
    if filter == "json":
        filter = "JSON files (*.json)|*.json||"
    elif filter == "obj":
        filter = "OBJ files (*.obj)|*.obj||"
    elif filter == "fofin":
        filter = "FOFIN session files (*.fofin)|*.fofin||"
    else:
        pass
    return rs.OpenFileName(title, filter=filter, folder=folder)


select_file = browse_for_file


def print_display_on(on=True):
    if on:
        rs.Command("_PrintDisplay State On Color Display Thickness 1 _Enter")
    else:
        rs.Command("_PrintDisplay State Off _Enter")


# def display_message(message):
#     return ShowMessageBox(message, "Message")


# def display_text(text, title="Text", width=800, height=600):
#     if isinstance(text, (list, tuple)):
#         text = "{0}".format(System.Environment.NewLine).join(text)
#     form = TextForm(text, title, width, height)
#     return form.show()


# def display_image(image, title="Image", width=800, height=600):
#     form = ImageForm(image, title, width, height)
#     return form.show()


# def display_html():
#     raise NotImplementedError


# ==============================================================================
# Settings and attributes
# ==============================================================================


# def update_named_values(names, values, message="", title="Update named values", evaluate=False):
#     values = ShowPropertyListBox(message, title, names, values)
#     if evaluate:
#         if values:
#             values = list(values)
#             for i in range(len(values)):
#                 value = values[i]
#                 try:
#                     value = ast.literal_eval(value)
#                 except (TypeError, ValueError, SyntaxError):
#                     pass
#                 values[i] = value
#     return values


# def update_settings(settings, message="", title="Update settings"):
#     names = sorted(settings.keys())
#     values = [str(settings[name]) for name in names]
#     values = update_named_values(names, values, message=message, title=title)
#     if values:
#         values = list(values)
#         for name, value in zip(names, values):
#             try:
#                 settings[name] = ast.literal_eval(value)
#             except (TypeError, ValueError, SyntaxError):
#                 settings[name] = value
#         return True
#     return False
