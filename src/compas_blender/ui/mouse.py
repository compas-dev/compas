import bpy


__all__ = [
    'Mouse',
]


class Mouse(object):

    def __init__(self):
        pass

    def OnMouseMove(self, e):
        raise NotImplementedError

    def OnMouseDown(self, e):
        raise NotImplementedError

    def OnMouseUp(self, e):
        raise NotImplementedError

    def xyz(self):
        return list(bpy.context.scene.cursor_location.copy())


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
