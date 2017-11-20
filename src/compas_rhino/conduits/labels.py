from __future__ import print_function

from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from System.Drawing.Color import FromArgb

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['LabelsConduit', ]


class LabelsConduit(Conduit):
    """A Rhino display conduit for labels.

    Parameters:
        labels (list): A list of label tuples. Each tuple contains a position and text for the label.
        color (tuple): Optional.
            RGB color spec for the dots.
            Default is ``None``.

    Example:

        .. code-block:: python

            from random import randint
            import time

            labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]

            try:
                conduit = LabelsConduit(labels)
                conduit.Enabled = True

                for i in range(100):
                    labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]
                    conduit.labels = labels

                    conduit.redraw()

                    time.sleep(0.1)

            except Exception as e:
                print e

            finally:
                conduit.Enabled = False
                del conduit

    """
    def __init__(self, labels, color=None, **kwargs):
        super(LabelsConduit, self).__init__(**kwargs)
        self.labels = labels
        color = color or (255, 255, 255)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        for pos, text in self.labels:
            e.Display.DrawDot(Point3d(*pos), text)


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]

    try:
        conduit = LabelsConduit(labels)
        conduit.Enabled = True

        for i in range(100):
            labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]
            conduit.labels = labels

            conduit.redraw()

            time.sleep(0.1)

    except Exception as e:
        print(e)

    finally:
        conduit.Enabled = False
        del conduit
