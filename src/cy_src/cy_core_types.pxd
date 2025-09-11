"""
core types used for the rest of the code -- e.g.

Point
Vector
PolyGon
"""


cdef class Point:
    cdef readonly double x, y


cdef class Vector:
    cdef readonly double x, y


# theses attributes cannot be accesed from Python
# "readonly" or "public" could be added if need be.

cdef class Interval:
    cdef double xmin, xmax


cdef class Box:
    cdef double xmin, xmax, ymin, ymax


cdef class Triangle:
    cdef Point a, b, c
