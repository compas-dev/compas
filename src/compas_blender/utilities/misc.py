
try:
    import bpy
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'display_message',
    'display_text',
    'display_image',
    'display_html',
    'browse_for_file',
    'browse_for_folder',
    'get_tolerance',
    'screenshot_current_view',
    'update_settings',
    'update_attributes',
    'update_named_values',
    'wait',
]


# ==============================================================================
# Misc
# ==============================================================================

def get_tolerance():

    raise NotImplementedError


def screenshot_current_view():

    raise NotImplementedError


def wait():

    raise NotImplementedError


# ==============================================================================
# File system
# ==============================================================================


def browse_for_folder():

    raise NotImplementedError



def browse_for_file():

    raise NotImplementedError


# ==============================================================================
# Display
# ==============================================================================

def display_message():

    raise NotImplementedError


def display_text():

    raise NotImplementedError


def display_image():

    raise NotImplementedError


def display_html():

    raise NotImplementedError


# ==============================================================================
# Settings and attributes
# ==============================================================================

def update_settings():

    raise NotImplementedError


def update_attributes():

    raise NotImplementedError


def update_named_values():

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
