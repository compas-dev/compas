
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [
    'FaceSelector',
]


class FaceSelector(object):

    @staticmethod
    def select_face(self, message="Select a face."):

        raise NotImplementedError


    @staticmethod
    def select_faces(self, message="Select faces."):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
