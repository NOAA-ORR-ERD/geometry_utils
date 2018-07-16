
"""
Cython code to call C point in poly routine

Should I just port the C to Cython???

And a polygon_area function

"""


import cython
# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as cnp

# declare the interface to the C code
cdef extern char c_point_in_poly1(size_t nvert, double *vertices, double *point)


@cython.boundscheck(False)
@cython.wraparound(False)
def point_in_poly(cnp.ndarray[double, ndim=2, mode="c"] poly not None,
                   in_point):
    """
    point_in_poly( poly, in_point )

    Determines if point is in the polygon -- 1 if it is, 0 if not

    :param poly: A Nx2 numpy array of doubles.
    :param point: A (x,y) sequence of floats (doubles, whatever)

    NOTE: points on the boundary are arbitrarily (fp errors..),
          but consistently considered either in or out, so that a given point
          should be in only one of two polygons that share a boundary.

    This calls C code I adapted from here:
    http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
    """
    cdef size_t nvert
    cdef char result
    cdef double[2] point

    point[0] = in_point[0]
    point[1] = in_point[1]

    nvert = poly.shape[0]

    result = c_point_in_poly1(nvert, &poly[0, 0], point)

    return result


@cython.boundscheck(False)
@cython.wraparound(False)
def points_in_poly(cnp.ndarray[double, ndim=2, mode="c"] pgon, points):
    """
    compute whether the points given are in the polygon defined in pgon.

    :param pgon: the vertices of the polygon
    :type pgon: NX2 numpy array of floats

    :param points: the points to test
    :type points: NX3 numpy array of (x, y, z) floats

    :returns: a boolean array the same length as points
              if the input is a single point, the result is a
              scalar python boolean
    """

    np_points = np.ascontiguousarray(points, dtype=np.float64)
    scalar = (np_points.shape == (2,))
    np_points.shape = (-1, 2)

    cdef double [:, :] a_points
    a_points = np_points

    ## fixme -- proper way to get np.bool?
    cdef cnp.ndarray[char, ndim = 1, mode = "c"] result = np.zeros((a_points.shape[0],), dtype=np.uint8)

    cdef unsigned int i, nvert, npoints

    nvert = pgon.shape[0]
    npoints = a_points.shape[0]

    for i in range(npoints):
        result[i] = c_point_in_poly1(nvert, &pgon[0, 0], &a_points[i, 0])

    if scalar:
        return bool(result[0])  # to make it a regular python bool
    else:
        return result.view(dtype=np.bool)  # make it a np.bool array

@cython.boundscheck(False)
@cython.wraparound(False)
def points_in_polys(cnp.ndarray[double, ndim=3, mode="c"] pgons,
                    cnp.ndarray[double, ndim=2, mode="c"] points):
    """
    Determine if a list of points is inside a list of polygons, in a one-to-one fashion.

    :param pgon: N records of M vertices per polygon
    :type pgon: NxMx2 numpy array of floats

    :param points: the points to test
    :type points: NX2 numpy array of (x, y) floats

    :returns: a boolean array of length N
    """
    cdef unsigned int i, N, M
    cdef cnp.ndarray[char, ndim=1, mode="c"] result

    result = np.zeros((points.shape[0],), dtype=np.uint8)

    M = pgons.shape[1]
    N = pgons.shape[0]

    for i in range(N):
        result[i] = c_point_in_poly1(M, &pgons[i, 0, 0], &points[i, 0])

    return result.view(dtype=np.bool)


@cython.boundscheck(False)
@cython.wraparound(False)
def signed_area(cnp.ndarray[double, ndim=2, mode="c"] polygon_verts):
    """
    Compute the signed area of the polygon defined by the vertices in pgon

    :param polygon_verts: the vertices of the polygon
    :type polygon_verts: NX2 numpy array of floats

    :returns: area of the polygon as a float64

    See: http://paulbourke.net/geometry/clockwise/
    """

    cdef unsigned int i, nvert
    cdef double total

    nvert = polygon_verts.shape[0]

    total = ((polygon_verts[nvert - 1, 0] * polygon_verts[0, 1]) -
             (polygon_verts[0, 0] * polygon_verts[nvert - 1, 1])
             )  # last point to first point

    for i in range(nvert - 1):
        total += ((polygon_verts[i, 0] * polygon_verts[i + 1, 1]) -
                  (polygon_verts[i + 1, 0] * polygon_verts[i, 1])
                  )

    return total / 2.0

