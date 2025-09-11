
"""
Cython code to call C point in poly routine

Should I just port the C to Cython???

And a polygon_area function

"""

# cython: language_level=3

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
    cdef cnp.ndarray[char, ndim=1, mode="c"] result = np.zeros((a_points.shape[0],), dtype=np.uint8)

    cdef unsigned int i, nvert, npoints

    nvert = pgon.shape[0]
    npoints = a_points.shape[0]

    for i in range(npoints):
        result[i] = c_point_in_poly1(nvert, &pgon[0, 0], &a_points[i, 0])

    if scalar:
        return bool(result[0])  # to make it a regular python bool
    else:
        return result.view(dtype=np.bool_)  # make it a np.bool array

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

    return result.view(dtype=np.bool_)


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

@cython.boundscheck(False)
@cython.wraparound(False)
def polygon_centroid(cnp.ndarray[double, ndim=2, mode="c"] polygon_verts):
    """
    Return the (x, y) location of the polygon centroid

    This is the "center of gravity" centroid -- it will not necessarily
    fall inside the polygon for concave polygons.

    INPUT
    -----
    polygon_verts:  (N,2) array of float64

    OUTPUT
    ------
    xy_centroid:  (2,)

    """

    # this is computing the area and the centroids of each area segment at the
    # same time so it is the same code as the area, with a bit of extra

    cdef unsigned int i, nvert
    cdef double area, a, x, y

    nvert = polygon_verts.shape[0]
    x = 0.0
    y = 0.0

    # last point to first point
    # could probably do this by setting indexes smarter ...
    # rather than duplicating code.
    area = ((polygon_verts[nvert - 1, 0] * polygon_verts[0, 1])
            - (polygon_verts[0, 0] * polygon_verts[nvert - 1, 1])
            )
    x += (polygon_verts[nvert - 1, 0] + polygon_verts[0, 0]) * area
    y += (polygon_verts[nvert - 1, 1] + polygon_verts[0, 1]) * area

    for i in range(nvert - 1):
        a = ((polygon_verts[i, 0] * polygon_verts[i + 1, 1])
             - (polygon_verts[i + 1, 0] * polygon_verts[i, 1])
             )
        area += a
        x += (polygon_verts[i, 0] + polygon_verts[i + 1, 0]) * a
        y += (polygon_verts[i, 1] + polygon_verts[i + 1, 1]) * a

    area /= 2.0
    x /= (6.0 * area)
    y /= (6.0 * area)

    return (x, y)

# Polygon clipping:
#
# Code and tests adapted from the numba_celltree project:
#
# https://github.com/Deltares/numba_celltree

"""
Sutherland-Hodgman clipping
---------------------------
Vertices (always lower case, single letter):
Clipping polygon with vertices r, s, ...
Subject polgyon with vertices a, b, ...
Vectors (always upper case, single letter):

* U: r -> s
* N: norm, orthogonal to u
* V: a -> b
* W: a -> r

   s ----- ...
   |
   |  b ----- ...
   | /
   |/
   x
  /|
 / |
a--+-- ...
   |
   r ----- ...

Floating point rounding should not be an issue, since we're only looking at
finding the area of overlap of two convex polygons.
In case of intersection failure, we can ignore it when going out -> in. It will
occur when the outgoing point is very close the clipping edge. In that case the
intersection point ~= vertex b, and we can safely skip the intersection.
When going in -> out, b might be located on the edge. If intersection fails,
again the intersection point ~= vertex b. We treat b as if it is just on the
inside and append it. For consistency, we set b_inside to True, as it will be
used as a_inside in the next iteration.
"""

from typing import Sequence, Tuple

import numpy as np

# from numba_celltree.constants import PARALLEL, FloatArray, FloatDType, IntArray
# from numba_celltree.geometry_utils import (
#     Point,
#     Vector,
#     as_box,
#     as_point,
#     copy_box_vertices,
#     copy_vertices,
#     dot_product,
#     polygon_area,
# )
# from numba_celltree.utils import allocate_clip_polygon, copy

cdef inline float dot_product(u: double[2], v: double[2]):
    return u[0] * v[0] + u[1] * v[1]

# @nb.njit(inline="always")
cpdef bint inside(p: double[2], r: double[2], U: double[2]):
    # U: a -> b direction vector
    # p is point r or s
    return U[0] * (p[1] - r[1]) > U[1] * (p[0] - r[0])

# @nb.njit(inline="always")
cpdef tuple intersection(a: double[2], V: Vector, r: double[2], N: Vector):
    # Find the intersection with an (infinite) clipping plane
    cdef double[2] W = np.array((r[0] - a[0], r[1] - a[1]), dtype=np.float64)
    cdef double[2] result
    nw = dot_product(N, W)
    nv = dot_product(N, V)
    if nv != 0:
        t = nw / nv
        result = np.array((a[0] + t * V[0], a[1] + t * V[1]), dtype=np.float64)
        return True, result
    else:
        # parallel lines
        return False, np.array((np.nan, np.nan), dtype=np.float64)

# def intersection(a: Point, V: Vector, r: Point, N: Vector) -> Tuple[bool, Point]:
#     # Find the intersection with an (infinite) clipping plane
#     W = Vector(r.x - a.x, r.y - a.y)
#     nw = dot_product(N, W)
#     nv = dot_product(N, V)
#     if nv != 0:
#         t = nw / nv
#         return True, Point(a.x + t * V.x, a.y + t * V.y)
#     else:
#         # parallel lines
#         return False, Point(np.nan, np.nan)


# @nb.njit(inline="always")
# def push_point(polygon: FloatArray, size: int, p: Point) -> int:
#     # polygon[size][0] = p.x
#     # polygon[size][1] = p.y
#     # return size + 1
cdef inline int push_point(polygon: double[:,:], size: int, p: double[2]):
    polygon[size,0] = p[0]
    polygon[size,1] = p[1]
    return size + 1


# @nb.njit(inline="always")
def polygon_polygon_clip_area(polygon: Sequence, clipper: Sequence) -> float:
    pass
    # n_output = len(polygon)
    # n_clip = len(clipper)
    # subject = allocate_clip_polygon()
    # output = allocate_clip_polygon()

    # # Copy polygon into output
    # copy(polygon, output, n_output)

    # # Grab last point
    # r = as_point(clipper[n_clip - 1])
    # for i in range(n_clip):
    #     s = as_point(clipper[i])

    #     U = Vector(s.x - r.x, s.y - r.y)
    #     if U.x == 0 and U.y == 0:
    #         continue
    #     N = Vector(-U.y, U.x)

    #     # Copy output into subject
    #     length = n_output
    #     copy(output, subject, length)
    #     # Reset
    #     n_output = 0
    #     # Grab last point
    #     a = as_point(subject[length - 1])
    #     a_inside = inside(a, r, U)
    #     for j in range(length):
    #         b = as_point(subject[j])

    #         V = Vector(b.x - a.x, b.y - a.y)
    #         if V.x == 0 and V.y == 0:
    #             continue

    #         b_inside = inside(b, r, U)
    #         if b_inside:
    #             if not a_inside:  # out, or on the edge
    #                 succes, point = intersection(a, V, r, N)
    #                 if succes:
    #                     n_output = push_point(output, n_output, point)
    #             n_output = push_point(output, n_output, b)
    #         elif a_inside:
    #             succes, point = intersection(a, V, r, N)
    #             if succes:
    #                 n_output = push_point(output, n_output, point)
    #             else:  # Floating point failure
    #                 # TODO: haven't come up with a test case yet to succesfully
    #                 # trigger this ...
    #                 b_inside = True  # flip it for consistency, will be set as a
    #                 n_output = push_point(output, n_output, b)  # push b instead

    #         # Advance to next polygon edge
    #         a = b
    #         a_inside = b_inside

    #     # Exit early in case not enough vertices are left.
    #     if n_output < 3:
    #         return 0.0

    #     # Advance to next clipping edge
    #     r = s

    # area = polygon_area(output[:n_output])
    # return area


# @nb.njit(parallel=PARALLEL, cache=True)
def area_of_intersection(
    vertices_a: FloatArray,
    vertices_b: FloatArray,
    faces_a: IntArray,
    faces_b: IntArray,
    indices_a: IntArray,
    indices_b: IntArray,
) -> FloatArray:
    pass
    # n_intersection = indices_a.size
    # area = np.empty(n_intersection, dtype=FloatDType)
    # for i in nb.prange(n_intersection):
    #     face_a = faces_a[indices_a[i]]
    #     face_b = faces_b[indices_b[i]]
    #     a = copy_vertices(vertices_a, face_a)
    #     b = copy_vertices(vertices_b, face_b)
    #     area[i] = polygon_polygon_clip_area(a, b)
    # return area


# @nb.njit(parallel=PARALLEL, cache=True)
def box_area_of_intersection(
    bbox_coords: FloatArray,
    vertices: FloatArray,
    faces: IntArray,
    indices_bbox: IntArray,
    indices_face: IntArray,
) -> FloatArray:
    pass
    # n_intersection = indices_bbox.size
    # area = np.empty(n_intersection, dtype=FloatDType)
    # for i in nb.prange(n_intersection):
    #     box = as_box(bbox_coords[indices_bbox[i]])
    #     face = faces[indices_face[i]]
    #     a = copy_box_vertices(box)
    #     b = copy_vertices(vertices, face)
    #     area[i] = polygon_polygon_clip_area(a, b)
    # return area


