#!/usr/bin/env python

"""
Single module to hold the high-level API for working with polygons
"""

import numpy as np

from . import cy_polygons as cyp

from .import cy_line_crossings as clc


def polygon_inside(polygon_verts, trial_points):
    '''
    Return a Boolean array the size of the trial point array True if point is inside

    INPUTS
    ------
    polygon_verts:  Nx2 array
    trial_points:   Single point: len-2 seq (x, y) or multiple_points: Nx2 array

    RETURNS
    -------
    inside_points:  Boolean array (len(N))
                    True if the trial point is inside the polygon
                    If input it single point, a single bool is returned
    '''

    polygon_verts = np.asarray(polygon_verts, dtype=np.float64)
    trial_points = np.asarray(trial_points, dtype=np.float64)
    return cyp.points_in_poly(polygon_verts, trial_points)


def polygon_area(polygon_verts):
    """
    Calculate the area of a polygon


    INPUTS
    ------
    polygon_verts:  Nx2 array

    Sequence of tuples, or something like it (Nx2 array for instance),
    of the points:

    [ (x1, y1), (x2, y2), (x3, y3), ...(xi, yi) ]

    Computes the signed area -- the sign is CW or CCW
    See: http://paulbourke.net/geometry/clockwise/
    """

    polygon_verts = np.asarray(polygon_verts, np.float64)
    return abs(cyp.signed_area(polygon_verts))


def polygon_is_simple(polygon_verts):
    '''
    Return true if the polygon is simple

    i.e. has no crossing segments, etc.

    NOTE: This version is naive, and O(N^2).
          It simply checks each segment against all the other segments.

    Possible better option:
    Shamos-Hoey algorithm:
    https://web.archive.org/web/20060613060645/http://softsurfer.com/Archive/algorithm_0108/algorithm_0108.htm#Test%20if%20Simple
    '''

    polygon_verts = np.asarray(polygon_verts)

    # make sure first and final point are duplicated
    # note: this does require an unfortunate reallocation
    # maybe deal with last segment separately?
    if not np.array_equal(polygon_verts[0], polygon_verts[-1]):
        polygon_verts = np.r_[polygon_verts, polygon_verts[:1]]
    # loop through every line segment, and compare to every other one:
    for i1 in range(len(polygon_verts) - 1):
        seg1 = (polygon_verts[i1, :], polygon_verts[i1 + 1, :])
        for i2 in range(i1 + 1, len(polygon_verts) - 1):
            if (i2 == i1 + 1):
                # check for degenerate segment
                if np.array_equal(polygon_verts[i1, :], polygon_verts[i1 + 2, :],):
                    return False
                continue
            elif (i1 == 0) and (i2 == (len(polygon_verts) - 2)):  # the start and end segments
                # never occurs
                # the start and end segments
                # or ((i1 == (len(polygon_verts) - 2)) and (i2 == 0))
                # or (i2 == i1 - 1)
                # ):
                continue
            seg2 = (polygon_verts[i2, :], polygon_verts[i2 + 1, :])
            if clc.segment_cross(seg1, seg2):
                return False
    return True


def polygon_rotation(polygon_verts, convex=False):
    '''
    Return a int/bool flag indicating the "winding order" of the polygon

    i.e. clockwise or anti-clockwise

    INPUT
    -----
    polygon_verts:  Nx2 array

    convex=False: flag to indicate if the polygon is convex
                  -- if it is convex, a faster algorithm will be used.

    OUTPUT
    ------
    rotation:  scalar / boolean
               1 (cw) for a positive rotation according to the right-hand rule
               0 (ccw) for a negative rotation according to the right hand rule

               Note, only defined for a simple polygon. Behavior is undetermined
               if the polygon has holes or crossing segments.

    '''
    polygon_verts = np.asarray(polygon_verts, np.float64)
    s_a = cyp.signed_area(polygon_verts)
    if s_a < 0:
        return True
    elif s_a > 0:
        return False
    else:
        raise ValueError("can't compute rotation of a zero-area polygon")


def polygon_centroid(polygon_verts):
    """
    Return the (x, y) location of the polygon centroid

    This is the "center of gravity" centroid -- it will not necessarily
    fall inside the polygon for convex polygons.

    INPUT
    -----
    polygon_verts:  Nx2 array

    OUTPUT
    ------
    xy_centroid:  (2,)

    NOTE: implementation from:
    # https://stackoverflow.com/questions/2792443/finding-the-centroid-of-a-polygon
    """

    polygon_verts = np.asarray(polygon_verts, np.float64)
    return cyp.polygon_centroid(polygon_verts)




