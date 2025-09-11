"""
core types used for the rest of the code -- e.g.

Point
Vector
etc.

These are all ported over from numba_celltree -- useful here?

note: point and vector are the same, but kept separate to keep the use cases clear

maybe some day?

PolyGon
Rect
"""

cdef class Point:
    def __init__(self, x: double, y: double):
        self.x = x
        self.y = y
    def __getitem__(self, ind: int):
        if ind == 0:
            return self.x
        elif ind == 1:
            return self.y
        else:
            raise IndexError("Point can only be indexed with 0 or 1")

cdef class Vector:
    def __init__(self, x: double, y: double):
        self.x = x
        self.y = y
    def __getitem__(self, ind: int):
        if ind == 0:
            return self.x
        elif ind == 1:
            return self.y
        else:
            raise IndexError("Vector can only be indexed with 0 or 1")

# The following are from numba_celltree, and are used internally.
# They cannot (at this point) be accessed from Python

cdef class Interval:
    def __init__(self, xmin: double, xmax: double):
        self.xmin = xmin
        self.xmax = xmax


cdef class Box:
    def __init__(self, xmin: double, xmax: double, ymin: double, ymax:double):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax


cdef class Triangle:
    def __init__(self, a: Point, b: Point, c: Point,):
        self.a = a
        self.b = b
        self.c = c
