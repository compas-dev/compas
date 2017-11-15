from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['LinesConduit', ]


class LinesConduit(Conduit):
    """A Rhino display conduit for lines.

    Parameters:
        lines (list): A list of start-end point pairs that define the lines.
        thickness (float): Optional.
            The thickness of the conduit lines.
            Default is ``1.0``.
        color (tuple): Optional.
            RGB color spec for the conduit lines.
            Default is ``None``.

    Example:

        .. code-block:: python

            import random
            import time

            points = [(1.0 * random.ranint(0, 30), 1.0 * random.randint(0, 30), 0.0) for _ in range(100)]
            lines  = [(points[i], points[i + 1]) for i in range(99)]

            conduit = LinesConduit(lines)
            conduit.enable()

            try:
                for i in range(100):
                    points = [(1.0 * random.randint(0, 30), 1.0 * random.randint(0, 30), 0.0) for _ in range(100)]
                    conduit.lines = [(points[i], points[i + 1]) for i in range(99)]
                    conduit.redraw()

                    time.sleep(0.1)
            except:
                raise

            finally:
                conduit.disable()
                del conduit

    """
    def __init__(self, lines, thickness=1.0, color=None, **kwargs):
        super(LinesConduit, self).__init__(**kwargs)
        self.lines = lines
        self.n = len(lines)
        self.thickness = thickness
        color = color or (255, 255, 255)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        lines = List[Line](self.n)
        for start, end in self.lines:
            lines.Add(Line(Point3d(*start), Point3d(*end)))
        e.Display.DrawLines(lines, self.color, self.thickness)


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
    lines  = [(points[i], points[i + 1]) for i in range(99)]

    try:
        conduit = LinesConduit(lines)
        conduit.Enabled = True

        for i in range(100):
            points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
            conduit.lines = [(points[i], points[i + 1]) for i in range(99)]

            conduit.redraw()

            time.sleep(0.1)

    except Exception as e:
        print(e)

    finally:
        conduit.Enabled = False
        del conduit
