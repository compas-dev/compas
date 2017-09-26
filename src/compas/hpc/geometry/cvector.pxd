cdef class CVector:
    
    cdef double _x
    cdef double _y
    cdef double _z

    cpdef double length(CVector self)

    cpdef double dot(CVector u, object v)

    cpdef CVector cross(CVector u, object v)

    cpdef CVector normalize(CVector self)

    cpdef CVector normalized(CVector self)
