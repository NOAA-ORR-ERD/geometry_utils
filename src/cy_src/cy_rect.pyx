# cython: language_level=3

"""
Utilities for working with bounding rectangles

A rectangle is defined as a 2x2 numpy array of float64::

   [[min_x, min_y],
    [max_x, max_y]]

A zero-size rect is allowed.
"""

import cython
# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as cnp


cpdef rect(ll, ur):
    """
    make a rect compatible numpy array from two points

    :param ll: lower-left point (min_x, min_y)

    :param ur: upper_right point (max_x, max_y)

    :param ll: lower-left point (min_x, min_y)
    """
    cdef cnp.ndarray[double, ndim=2, mode="c"] rec

    rec = np.array([ll, ur], dtype=np.float64)

    return rec


@cython.boundscheck(False)
@cython.wraparound(False)
# cpdef from_points(cnp.ndarray[double, ndim=2, mode="c"] points):
cpdef from_points(const double [:,:] points):
    """
    from_points (points).

    returns a rect that's the bounding box of the set of points in points.
    points is a numpy NX2 array of float64s.

    If a single point is passed in, a zero-size Bounding Box is returned.
    """
    cdef cnp.ndarray[double, ndim=2, mode="c"] rect = np.empty((2,2), dtype=np.float64)
    cdef double [:,:] rectv = rect

    if points.shape[1] != 2:
        raise ValueError("points must be a Nx2 array of float64")

    rectv[0, 0] = points[0, 0]
    rectv[0, 1] = points[0, 1]
    rectv[1, 0] = points[0, 0]
    rectv[1, 1] = points[0, 1]

    cdef unsigned int i
    for i in range(points.shape[0]):
        if points[i, 0] < rectv[0, 0]:
            rectv[0, 0] = points[i, 0]
        if points[i, 1] < rectv[0, 1]:
            rectv[0, 1] = points[i, 1]

        if points[i, 0] > rectv[1, 0]:
            rectv[1, 0] = points[i, 0]
        if points[i, 1] > rectv[1, 1]:
            rectv[1, 1] = points[i, 1]


    # arr = np.vstack((points.min(0), points.max(0)))

    return rect


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef is_correct(cnp.ndarray[double, ndim=2, mode="c"] rect):

    # wrong shape raises
    if not (rect.shape[0] == 2 and rect.shape[1] == 2):
        raise ValueError("rect is the correct shape: should be 2x2")

    # Other errors simply return False
    if rect[0, 0] > rect[1, 0] or rect[0, 1] > rect[1, 1]:
        return False

    return True

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef intersect(cnp.ndarray[double, ndim=2, mode="c"] rect1,
                cnp.ndarray[double, ndim=2, mode="c"] rect2,
                ):
    """
    Tests if the two rects intersect (overlap).

    Returns True if the rects overlap, False otherwise

    If they are just touching, returns True
    """

    # if np.isinf(rect1).all() or np.isinf(rect2).all():
    #     return True
    if ((rect1[1, 0] >= rect2[0, 0]) and (rect1[0, 0] <= rect2[1, 0]) and
            (rect1[1, 1] >= rect2[0, 1]) and (rect1[0, 1] <= rect2[1, 1])):
        return True
    else:
        return False

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inside(cnp.ndarray[double, ndim=2, mode="c"] rect,
             cnp.ndarray[double, ndim=1, mode="c"] point,
             ):

    """
    Checks if the point is inside the rectangle

    :param rect: rect as a 2x2 numpy array of float64

    :param point: point as a (2,) numpy array of float64

    NOTE: This version considers points on the line as inside.
          It might be better to be open on right and top, so that
          the same point would not be in two adjacent rects.

    """
    if (point[0] >= rect[0, 0] and
        point[0] <= rect[1, 0] and
        point[1] <= rect[1, 1] and
        point[1] >= rect[0, 1]):
        return True
    else:
        return False


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef as_poly(cnp.ndarray[double, ndim=2, mode="c"] rect,
             ):

        """
        Returns the four corners of the bounding box as polygon:

        An 4X2 array of (x, y) coordinates of the corners
        """
        cdef cnp.ndarray[double, ndim=2, mode="c"] poly

        poly = np.array(((rect[0, 0], rect[0, 1]),
                         (rect[0, 0], rect[1, 1]),
                         (rect[1, 0], rect[1, 1]),
                         (rect[1, 0], rect[0, 1]),
                         ), dtype=np.float64)
        return poly

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef merge(cnp.ndarray[double, ndim=2, mode="c"] rect1,
            cnp.ndarray[double, ndim=2, mode="c"] rect2,
            ):

        """
        Joins two rects, maybe making a larger one
        """
        # hmm, I could have used from_points for this -- slightly faster this way?
        cdef cnp.ndarray[double, ndim=2, mode="c"] rect3 = np.array(rect1)

        if rect2[0, 0] < rect3[0, 0]:
            rect3[0, 0] = rect2[0, 0]
        if rect2[0, 1] < rect3[0, 1]:
            rect3[0, 1] = rect2[0, 1]
        if rect2[1, 0] > rect3[1, 0]:
            rect3[1, 0] = rect2[1, 0]
        if rect2[1, 1] > rect3[1, 1]:
            rect3[1, 1] = rect2[1, 1]

        return rect3



