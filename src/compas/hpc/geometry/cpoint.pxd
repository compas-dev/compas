cdef class CPoint:

    cdef double _x
    cdef double _y
    cdef double _z

    cpdef double distance_to_point(CPoint a, object b)
    cpdef double distance_to_line(CPoint point, object line)
