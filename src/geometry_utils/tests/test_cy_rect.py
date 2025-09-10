#!/usr/bin/env python

"""
Test code for rectangle functions

NOTE: a "rect" is a 2x2 numpy array of dtype float64::

  [[min_x, min_y],
   [max_x, max_y]]

"""

import numpy as np
import pytest

from geometry_utils.utilities import point
from geometry_utils import cy_rect as rect

# def point(x, y):
#     """
#     makes a compatible numpy array -- makes testing easier
#     """
#     return np.array((x, y), dtype=np.float64)

def test_from_points():
        pts = np.array(((5, 2), (3, 4), (1, 6)), np.float64)

        rec = rect.from_points(pts)

        print(rec)

        assert rec.shape == (2, 2)
        assert rec.dtype == np.float64
        assert (rec[0, 0] == 1.0 and
                rec[0, 1] == 2.0 and
                rec[1, 0] == 5.0 and
                rec[1, 1] == 6.0)

def test_from_points_single():
    """
    passing a single point should create a size-zero bounding box
    """
    rec = rect.from_points(np.array(((5, 2),), np.float64))

    assert rec.shape == (2, 2)
    assert rec.dtype == np.float64
    assert (rec[0, 0] == 5.0 and
            rec[0, 1] == 2.0 and
            rec[1, 0] == 5.0 and
            rec[1, 1] == 2.0)

def test_from_points_out_of_order_bb():
    """
    passing a single point should create a size-zero bounding box

    A rect with the min and max backwards should work.
    """
    rec = rect.from_points(np.array(((5, 2),(3, 1)), np.float64))

    assert rec.shape == (2, 2)
    assert rec.dtype == np.float64
    assert (rec[0, 0] == 3.0 and
            rec[0, 1] == 1.0 and
            rec[1, 0] == 5.0 and
            rec[1, 1] == 2.0)


def test_is_correct_wrong_shape():
    """
    If the array is the wrong size, an error is raised
    """
    with pytest.raises(ValueError):
        rect.is_correct(np.array(((4, 5, 6), (10, 12, 13)), np.float64))


@pytest.mark.parametrize('rec', [np.array(((4, 5), (10, 12)), np.float64),
                                 np.array(((-10, -12), (-4, -5)), np.float64),
                                 np.array(((10, 5), (10, 12)), np.float64),  # size zero allowed
                                 np.array(((10, 5), (12, 5)), np.float64),  # size zero allowed
                                 np.array(((10, 12), (10, 12)), np.float64),  # size zero allowed
                                 np.array(((10, 10), (10, 10)), np.float64),  # size zero allowed
                                 np.array(((0, 0), (1e-200, 5)), np.float64), #tiny OK
                                 ])
def test_rect_is_correct(rec):
    """
    should return false if the rect is not correct:

    e.g. zero area, min/ max not correct.
    """
    print(rec)
    print(f"{(rec[0, 0] > rec[1, 0])=}")
    print(f"{(rec[0, 1] > rec[1, 1])=}")
    assert rect.is_correct(rec)


@pytest.mark.parametrize('rec', [np.array(((10, 12), (4, 5)), np.float64),
                                 np.array(((0, 0), (-1, 6)), np.float64),
                                 np.array(((10, 12), (10, 5)), np.float64),
                                 np.array(((0, 0), (-1e-200, 5)), np.float64),  # tiny in wrong way
                                 ])
def test_rect_is_not_correct(rec):

    assert not rect.is_correct(rec)


@pytest.mark.parametrize('rec1, rec2', [(rect.rect((-23.5, 456), (56, 532.0)),  # identical
                                         rect.rect((-23.5, 456), (56, 532.0))),
                                        (rect.rect((5, 10), (15, 25)),  # upper left
                                         rect.rect((0, 12), (10, 32.0))),
                                        (rect.rect((5, 10), (15, 25)),  # upper right
                                         rect.rect((12, 12), (25, 32.0))),
                                        (rect.rect((5, 10), (15, 25)),  # lower right
                                         rect.rect((12, 5), (25, 15))),
                                        (rect.rect((5, 10), (15, 25)),  # lower left
                                         rect.rect((-10, 5), (8.5, 15))),
                                        (rect.rect((-15, -25), (-5, -10)),  # inside
                                         rect.rect((-12, -22), (-6, -8))),
                                        (rect.rect((-15, -25), (-5, -10)),  # outside
                                         rect.rect((-17, -26), (3, 0))),
                                        (rect.rect((5, 10), (15, 25)),  # touch
                                         rect.rect((15, 8), (17.95, 32))),
                                        (rect.rect((5, 10), (15, 25)),  # touch corner
                                         rect.rect((15, 25), (17.95, 32))),
                                        ])
def test_intersect(rec1, rec2):
    assert rect.intersect(rec1, rec2)

@pytest.mark.parametrize('rec1, rec2', [(rect.rect((5, 10), (15, 25)),  # below
                                         rect.rect((-10, 5), (8.5, 9.2))),
                                        (rect.rect((5, 10), (15, 25)),  # above
                                         rect.rect((-10, 25.001), (8.5, 32))),
                                        (rect.rect((5, 10), (15, 25)),  # left
                                         rect.rect((4, 8), (4.95, 32))),
                                        (rect.rect((5, 10), (15, 25)),  # right
                                         rect.rect((17.1, 8), (17.95, 32))),
                                        ])
def test_not_intersect(rec1, rec2):
    assert not rect.intersect(rec1, rec2)

@pytest.mark.parametrize('point', [point(3.0, 4.0),
                                   point(3.0, 10.0),  # on top line
                                   ])
def test_inside(point):
    rec = rect.rect((1.0, 2.0), (5., 10.))
    assert rect.inside(rec, point)

#     def testPointLeftTopLine(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         P = (-3.0, 10.)
#         assert not (B.PointInside(P))


@pytest.mark.parametrize('point', [point(10.0, 5.0),  # below
                                   point(4, 30),  # upper left
                                   point(4, 30),  # upper right
                                   point(16, 4),  # lower right
                                   point(-10, 5),  # lower left
                                   point(10, 9.99999), # below
                                   point(10, 25.001), # above
                                   point(-3.0, 10.), # left of top line
                                   ])
def test_not_inside(point):

    rec = rect.rect((5, 10), (15, 25))
    assert not rect.inside(rec, point)


def test_as_poly():
    rec = rect.rect((5, 0), (10, 20))
    corners = np.array([(5., 0.), (5., 20.), (10., 20.), (10., 0.)],
                       dtype=np.float64)

    assert np.array_equal(rect.as_poly(rec), corners)

class TestMerge():

    A = rect.rect((-23.5, 456), (56, 532.0))
    B = rect.rect((-20.3, 460), (54, 465))   # B should be completely inside A
    C = rect.rect((-23.5, 456), (58, 540.))  # up and to the right or A
    D = rect.rect((-26.5, 12), (56, 532.0))

    def testInside(self):
        C = rect.merge(self.A, self.B)
        assert np.array_equal(C, self.A)

    def testFullOutside(self):
        # same but reversed
        C = rect.merge(self.B, self.A)
        assert np.array_equal(C, self.A)

    def testUpRight(self):
        A = self.A.copy()
        A = rect.merge(self.A, self.C)
        assert (A[0,0] == self.A[0,0]
                and A[0,1] == self.A[0,1]
                and A[1,0] == self.C[1,0]
                and A[1,1] == self.C[1,1])

    def testDownLeft(self):
        A = rect.merge(self.A, self.D)
        assert (A[0,0] == self.D[0,0]
                and A[0,1] == self.D[0,1]
                and A[1,0] == self.A[1,0]
                and A[1,1] == self.A[1,1])



# Do we need all these tests? I got lazy ...

#     def testLeft(self):
#         B = BBox(((5, 10), (15, 25)))
#         P = (4, 12)
#         assert not (B.PointInside(P))

#     def testRight(self):
#         B = BBox(((5, 10), (15, 25)))
#         P = (17.1, 12.3)
#         assert not (B.PointInside(P))

#     def testPointOnTopLine(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         P = (3.0, 10.)
#         assert (B.PointInside(P))

#     def testPointLeftTopLine(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         P = (-3.0, 10.)
#         assert not (B.PointInside(P))

#     def testPointOnBottomLine(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         P = (3.0, 5.)
#         assert (B.PointInside(P))

#     def testPointOnLeft(self):
#         B = BBox(((-10., -10.), (-1.0, -1.0)))
#         P = (-10, -5.)
#         assert (B.PointInside(P))

#     def testPointOnRight(self):
#         B = BBox(((-10., -10.), (-1.0, -1.0)))
#         P = (-1, -5.)
#         assert (B.PointInside(P))

#     def testPointOnBottomRight(self):
#         B = BBox(((-10., -10.), (-1.0, -1.0)))
#         P = (-1, -10.)
#         assert (B.PointInside(P))




# needed ???
#     def testZeroSize(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((15, 25), (15, 25)))
#         assert B.Overlaps(C)

#     def testZeroSize2(self):
#         B = BBox(((5, 10), (5, 10)))
#         C = BBox(((15, 25), (15, 25)))
#         assert not B.Overlaps(C)

#     def testZeroSize3(self):
#         B = BBox(((5, 10), (5, 10)))
#         C = BBox(((0, 8), (10, 12)))
#         assert B.Overlaps(C)

#     def testZeroSize4(self):
#         B = BBox(((5, 1), (10, 25)))
#         C = BBox(((8, 8), (8, 8)))
#         assert B.Overlaps(C)

# do we need an inside / outside check??
# class TestInside():

#     def testSame(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         C = BBox(((1.0, 2.0), (5., 10.)))
#         assert B.Inside(C)

#     def testPoint(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         C = BBox(((3.0, 4.0), (3.0, 4.0)))
#         assert B.Inside(C)

#     def testPointOutside(self):
#         B = BBox(((1.0, 2.0), (5., 10.)))
#         C = BBox(((-3.0, 4.0), (0.10, 4.0)))
#         assert not B.Inside(C)

#     def testUpperLeft(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((0, 12), (10, 32.0)))
#         assert not B.Inside(C)

#     def testUpperRight(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((12, 12), (25, 32.0)))
#         assert not B.Inside(C)

#     def testLowerRight(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((12, 5), (25, 15)))
#         assert not B.Inside(C)

#     def testLowerLeft(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((-10, 5), (8.5, 15)))
#         assert not (B.Inside(C))

#     def testBelow(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((-10, 5), (8.5, 9.2)))
#         assert not (B.Inside(C))

#     def testAbove(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((-10, 25.001), (8.5, 32)))
#         assert not (B.Inside(C))

#     def testLeft(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((4, 8), (4.95, 32)))
#         assert not (B.Inside(C))

#     def testRight(self):
#         B = BBox(((5, 10), (15, 25)))
#         C = BBox(((17.1, 8), (17.95, 32)))
#         assert not (B.Inside(C))


# class Test_from_points():

#     def testCreate(self):
#         Pts = np.array(((5, 2), (3, 4), (1, 6)), np.float64)
#         B = from_points(Pts)

#         assert (B[0, 0] == 1.0 and
#                 B[0, 1] == 2.0 and
#                 B[1, 0] == 5.0 and
#                 B[1, 1] == 6.0)

#     def testCreateInts(self):
#         Pts = np.array(((5, 2), (3, 4), (1, 6)))
#         B = from_points(Pts)
#         assert (B[0, 0] == 1.0 and
#                 B[0, 1] == 2.0 and
#                 B[1, 0] == 5.0 and
#                 B[1, 1] == 6.0)

#     def testSinglePoint(self):
#         Pts = np.array((5, 2), np.float64)
#         B = from_points(Pts)
#         assert (B[0, 0] == 5. and
#                 B[0, 1] == 2.0 and
#                 B[1, 0] == 5. and
#                 B[1, 1] == 2.0)

#     def testListTuples(self):
#         Pts = [(3, 6.5), (13, 43.2), (-4.32, -4), (65, -23), (-0.0001, 23.432)]
#         B = from_points(Pts)
#         assert (B[0, 0] == -4.32
#                 and B[0, 1] == -23.0
#                 and B[1, 0] == 65.0
#                 and B[1, 1] == 43.2)


# class TestMerge():

#     A = BBox(((-23.5, 456), (56, 532.0)))
#     B = BBox(((-20.3, 460), (54, 465)))   # B should be completely inside A
#     C = BBox(((-23.5, 456), (58, 540.)))  # up and to the right or A
#     D = BBox(((-26.5, 12), (56, 532.0)))

#     def testInside(self):
#         C = self.A.copy()
#         C.Merge(self.B)
#         assert (C == self.A)

#     def testFullOutside(self):
#         C = self.B.copy()
#         C.Merge(self.A)
#         assert (C == self.A)

#     def testUpRight(self):
#         A = self.A.copy()
#         A.Merge(self.C)
#         assert (A[0] == self.A[0] and A[1] == self.C[1])

#     def testDownLeft(self):
#         A = self.A.copy()
#         A.Merge(self.D)
#         assert (A[0] == self.D[0] and A[1] == self.A[1])


# class TestWidthHeight():

#     B = BBox(((1.0, 2.0), (5., 10.)))

#     def testWidth(self):
#         assert (self.B.Width == 4.0)

#     def testWidth2(self):
#         assert (self.B.Height == 8.0)

#     def testSetW(self):
#         with pytest.raises(AttributeError):
#             self.B.Height = 6

#     def testSetH(self):
#         with pytest.raises(AttributeError):
#             self.B.Width = 6


# class TestCenter():

#     B = BBox(((1.0, 2.0), (5., 10.)))

#     def testCenter(self):
#         assert ((self.B.Center == (3.0, 6.0)).all())

#     def testSetCenter(self):
#         with pytest.raises(AttributeError):
#             self.B.Center = (6, 5)


# class TestBBarray():

#     BBarray = np.array((((-23.5, 456), (56, 532.0)), ((-20.3, 460),
#                        (54, 465)), ((-23.5, 456), (58, 540.)), ((-26.5,
#                        12), (56, 532.0))), dtype=np.float64)
#     BB = asBBox(((-26.5, 12.), (58., 540.)))

#     def testJoin(self):
#         BB = fromBBArray(self.BBarray)
#         assert BB == self.BB


# class TestNullBBox():

#     B1 = NullBBox()
#     B2 = NullBBox()
#     B3 = BBox(((1.0, 2.0), (5., 10.)))

#     def testValues(self):
#         assert (np.all(np.isnan(self.B1)))

#     def testIsNull(self):
#         assert (self.B1.IsNull)

#     def testEquals(self):
#         assert ((self.B1 == self.B2) is True)

#     def testNotEquals(self):
#         assert not self.B1 == self.B3

#     def testNotEquals2(self):
#         assert not self.B3 == self.B1

#     def testMerge(self):
#         C = self.B1.copy()
#         C.Merge(self.B3)
#         assert C == self.B3, 'merge failed, got: %s' % C

#     def testOverlaps(self):
#         assert self.B1.Overlaps(self.B3) is False

#     def testOverlaps2(self):
#         assert self.B3.Overlaps(self.B1) is False


# class TestInfBBox():

#     B1 = InfBBox()
#     B2 = InfBBox()
#     B3 = BBox(((1.0, 2.0), (5., 10.)))
#     NB = NullBBox()

#     def testValues(self):
#         assert (np.all(np.isinf(self.B1)))

# #    def testIsNull(self):
# #        assert ( self.B1.IsNull )

#     def testEquals(self):
#         assert self.B1 == self.B2

#     def testNotEquals(self):
#         assert not self.B1 == self.B3

#     def testNotEquals2(self):
#         assert self.B1 != self.B3

#     def testNotEquals3(self):
#         assert not self.B3 == self.B1

#     def testMerge(self):
#         C = self.B1.copy()
#         C.Merge(self.B3)
#         assert C == self.B2, 'merge failed, got: %s' % C

#     def testMerge2(self):
#         C = self.B3.copy()
#         C.Merge(self.B1)
#         assert C == self.B1, 'merge failed, got: %s' % C

#     def testOverlaps(self):
#         assert (self.B1.Overlaps(self.B2) is True)

#     def testOverlaps2(self):
#         assert (self.B3.Overlaps(self.B1) is True)

#     def testOverlaps3(self):
#         assert (self.B1.Overlaps(self.B3) is True)

#     def testOverlaps4(self):
#         assert (self.B1.Overlaps(self.NB) is True)

#     def testOverlaps5(self):
#         assert (self.NB.Overlaps(self.B1) is True)


# class TestSides():

#     B = BBox(((1.0, 2.0), (5., 10.)))

#     def testLeft(self):
#         assert self.B.Left == 1.0

#     def testRight(self):
#         assert self.B.Right == 5.0

#     def testBottom(self):
#         assert self.B.Bottom == 2.0

#     def testTop(self):
#         assert self.B.Top == 10.0


# class TestAsPoly():

#     B = BBox(((5, 0), (10, 20)))
#     corners = np.array([(5., 0.), (5., 20.), (10., 20.), (10., 0.)],
#                        dtype=np.float64)

#     def testCorners(self):
#         print(self.B.AsPoly())
#         assert np.array_equal(self.B.AsPoly(), self.corners)
