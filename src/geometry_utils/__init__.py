"""
geometry package

This package has a collection of computional geometry routines

These routines are all designed to work with simple data types:

Python floats
numpy arrays

For the most parts, regular python sequences (lists, tuples) will be
converted to Python arrays for you when required.

i.e. a polygon is expressed as a Nx2 numpy array of float64

Some of these are in Cython for speed.
"""

__version__ = "0.1.0"

from .polygons import (polygon_inside,
                       polygon_area,
                       polygon_rotation,
                       polygon_centroid,
                       polygon_is_simple,
                       )
