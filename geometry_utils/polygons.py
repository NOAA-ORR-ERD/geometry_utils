#!/usr/bin/env python

"""
Single module to hold the high-level API
"""

import numpy as np

from .cy_point_in_polygon import points_in_poly, points_in_polys, signed_area


def polygon_inside(polygon_verts, trial_points):
    '''
    Return a Boolean array the size of the trial point array True if point is inside

    INPUTS
    ------
    polygon_verts:  Mx2 array
    trial_points:   Nx2 array

    RETURNS
    -------
    inside_points:  Boolean array (len(N))
                    True if the trial point is inside the polygon
    '''

    polygon_verts = np.asarray(polygon_verts, dtype=np.float)
    trial_points = np.asarray(trial_points, dtype=np.float)
    return points_in_poly(polygon_verts, trial_points)


def polygon_area(polygon_verts):
    """
    Calculate the area of a polygon

    expects a sequence of tuples, or something like it (Nx2 array for instance),
    of the points:

    [ (x1, y1), (x2, y2), (x3, y3), ...(xi, yi) ]

    See: http://paulbourke.net/geometry/clockwise/
    """

    # # note: this is the exact same code as the clockwise code.
    # #       they should both be cythonized and used in one place.

    # polygon_verts = np.asarray(polygon_verts, np.float64)
    # total = (polygon_verts[-1, 0] * polygon_verts[0, 1] -
    #          polygon_verts[0, 0] * polygon_verts[-1, 1])  # last point to first point

    # for i in range(len(polygon_verts) - 1):
    #     total += (polygon_verts[i, 0] * polygon_verts[i + 1, 1] -
    #               polygon_verts[i + 1, 0] * polygon_verts[i, 1])

    # return abs(total / 2.0)

    polygon_verts = np.asarray(polygon_verts, np.float64)
    return abs(signed_area(polygon_verts))


def polygon_issimple(polygon_verts):
    '''
    Return true if the polygon is simple

    i.e. has no holes, crossing segments, etc.
    '''

    # code
    raise NotImplementedError

    # return issimple


def polygon_rotation(polygon_verts, convex=False):
    '''
    Return a int/bool flag indicating the "winding order" of the polygon

    i.e. clockwise or anti-clockwise

    INPUT
    -----
    polygon_verts:  Mx2 array

    convex=False: flag to indicate if the polygon is convex
                  -- if it is convex, a faster algorithm will be used.

    OUTPUT
    ------
    rotation:  scalar / boolean
               1 for a positive rotation according to the right-hand rule
               0 for a negative rotation according to the right hand rule

              Note, only defined for a simple polygon. Raises error if not simple.

    '''
    # fixme: need test for simpile polygon!

    polygon_verts = np.asarray(polygon_verts, np.float64)
    s_a = signed_area(polygon_verts)
    if s_a < 0:
        return 1
    elif s_a > 0:
        return 0
    else:
        raise ValueError("can't compute rotation of a zero-area polygon")


def polygon_centroid(polygon_verts):
    '''
    Return the (x, y) location of the polygon centroid

    INPUT
    -----
    polygon_verts:  Mx2 array

    OUTPUT
    ------
    xy_centroid:  1x2

    '''

    raise NotImplementedError

