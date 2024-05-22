"""
geometry package

This package has:

A few higher-level objects for geometry: a Bounding Box class and a Polygon class.

It also has some lover level code basic geometry that acts on numpy arrays of points:

i.e. a polygon is expressed as a Nx2 numpy array of float64

Some of these are in Cython for speed.
"""

__version__ = "0.0.1dev"

from .polygons import (polygon_inside,
                       polygon_area,
                       polygon_rotation,
                       polygon_centroid,
                       polygon_is_simple,
                       )
