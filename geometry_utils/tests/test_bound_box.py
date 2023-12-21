#!/usr/bin/env python

"""
Test code for the BBox Object
"""

import numpy as np
import pytest

from geometry_utils.bound_box import (BBox,
                                      asBBox,
                                      NullBBox,
                                      InfBBox,
                                      fromBBArray,
                                      from_points,
                                      )


class TestConstructors():

    def test_creates(self):
        B = BBox(((0, 0), (5, 5)))
        assert isinstance(B, BBox)

    def test_type(self):
        B = np.array(((0, 0), (5, 5)))
        assert not isinstance(B, BBox)

    def testDataType(self):
        B = BBox(((0, 0), (5, 5)))
        assert B.dtype == np.float64

    def testShape(self):
        B = BBox((0, 0, 5, 5))
        assert B.shape == (2, 2)

    def testShape2(self):
        with pytest.raises(ValueError):
            BBox((0, 0, 5))

    def testShape3(self):
        with pytest.raises(ValueError):
            BBox((0, 0, 5, 6, 7))

    def testArrayConstruction(self):
        A = np.array(((4, 5), (10, 12)), np.float64)
        B = BBox(A)
        assert isinstance(B, BBox)

    def testMinMax(self):
        with pytest.raises(ValueError):
            BBox((0, 0, -1, 6))

    def testMinMax2(self):
        with pytest.raises(ValueError):
            BBox((0, 0, 1, -6))

    def testMinMax3(self):
        # OK to have a zero-sized BB

        B = BBox(((0, 0), (0, 5)))
        assert isinstance(B, BBox)

    def testMinMax4(self):
        # OK to have a zero-sized BB
        B = BBox(((10., -34), (10., -34.0)))
        assert isinstance(B, BBox)

    def testMinMax5(self):
        # OK to have a tiny BB
        B = BBox(((0, 0), (1e-20, 5)))
        assert isinstance(B, BBox)

    def testMinMax6(self):
        # Should catch tiny difference
        with pytest.raises(ValueError):
            BBox(((0, 0), (-1e-20, 5)))


class TestAsBBox():

    def testPassThrough(self):
        B = BBox(((0, 0), (5, 5)))
        C = asBBox(B)
        assert B is C

    def testPassThrough2(self):
        B = ((0, 0), (5, 5))
        C = asBBox(B)
        assert B is not C

    def testPassArray(self):
        # Different data type
        A = np.array(((0, 0), (5, 5)))
        C = asBBox(A)
        assert A is not C

    def testPassArray2(self):
        # same data type -- should be a view
        A = np.array(((0, 0), (5, 5)), np.float64)
        C = asBBox(A)
        A[0, 0] = -10
        assert C[0, 0] == A[0, 0]


class TestIntersect():

    def testSame(self):
        B = BBox(((-23.5, 456), (56, 532.0)))
        C = BBox(((-23.5, 456), (56, 532.0)))
        assert B.Overlaps(C)

    def testUpperLeft(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((0, 12), (10, 32.0)))
        assert B.Overlaps(C)

    def testUpperRight(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((12, 12), (25, 32.0)))
        assert B.Overlaps(C)

    def testLowerRight(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((12, 5), (25, 15)))
        assert B.Overlaps(C)

    def testLowerLeft(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((-10, 5), (8.5, 15)))
        assert B.Overlaps(C)

    def testBelow(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((-10, 5), (8.5, 9.2)))
        assert not B.Overlaps(C)

    def testAbove(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((-10, 25.001), (8.5, 32)))
        assert not B.Overlaps(C)

    def testLeft(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((4, 8), (4.95, 32)))
        assert not B.Overlaps(C)

    def testRight(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((17.1, 8), (17.95, 32)))
        assert not B.Overlaps(C)

    def testInside(self):
        B = BBox(((-15, -25), (-5, -10)))
        C = BBox(((-12, -22), (-6, -8)))
        assert B.Overlaps(C)

    def testOutside(self):
        B = BBox(((-15, -25), (-5, -10)))
        C = BBox(((-17, -26), (3, 0)))
        assert B.Overlaps(C)

    def testTouch(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((15, 8), (17.95, 32)))
        assert B.Overlaps(C)

    def testCorner(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((15, 25), (17.95, 32)))
        assert B.Overlaps(C)

    def testZeroSize(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((15, 25), (15, 25)))
        assert B.Overlaps(C)

    def testZeroSize2(self):
        B = BBox(((5, 10), (5, 10)))
        C = BBox(((15, 25), (15, 25)))
        assert not B.Overlaps(C)

    def testZeroSize3(self):
        B = BBox(((5, 10), (5, 10)))
        C = BBox(((0, 8), (10, 12)))
        assert B.Overlaps(C)

    def testZeroSize4(self):
        B = BBox(((5, 1), (10, 25)))
        C = BBox(((8, 8), (8, 8)))
        assert B.Overlaps(C)


class TestEquality():

    def testSame(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = BBox(((1.0, 2.0), (5., 10.)))
        assert B == C

    def testIdentical(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        assert B == B

    def testNotSame(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = BBox(((1.0, 2.0), (5., 10.1)))
        assert not B == C

    def testWithArray(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = np.array(((1.0, 2.0), (5., 10.)))
        assert B == C

    def testWithArray2(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = np.array(((1.0, 2.0), (5., 10.)))
        assert C == B

    def testWithArray3(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = np.array(((1.01, 2.0), (5., 10.)))
        assert not C == B


class TestInside():

    def testSame(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = BBox(((1.0, 2.0), (5., 10.)))
        assert B.Inside(C)

    def testPoint(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = BBox(((3.0, 4.0), (3.0, 4.0)))
        assert B.Inside(C)

    def testPointOutside(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        C = BBox(((-3.0, 4.0), (0.10, 4.0)))
        assert not B.Inside(C)

    def testUpperLeft(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((0, 12), (10, 32.0)))
        assert not B.Inside(C)

    def testUpperRight(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((12, 12), (25, 32.0)))
        assert not B.Inside(C)

    def testLowerRight(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((12, 5), (25, 15)))
        assert not B.Inside(C)

    def testLowerLeft(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((-10, 5), (8.5, 15)))
        assert not (B.Inside(C))

    def testBelow(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((-10, 5), (8.5, 9.2)))
        assert not (B.Inside(C))

    def testAbove(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((-10, 25.001), (8.5, 32)))
        assert not (B.Inside(C))

    def testLeft(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((4, 8), (4.95, 32)))
        assert not (B.Inside(C))

    def testRight(self):
        B = BBox(((5, 10), (15, 25)))
        C = BBox(((17.1, 8), (17.95, 32)))
        assert not (B.Inside(C))


class TestPointInside():

    def testPointIn(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        P = (3.0, 4.0)
        assert (B.PointInside(P))

    def testUpperLeft(self):
        B = BBox(((5, 10), (15, 25)))
        P = (4, 30)
        assert not (B.PointInside(P))

    def testUpperRight(self):
        B = BBox(((5, 10), (15, 25)))
        P = (16, 30)
        assert not (B.PointInside(P))

    def testLowerRight(self):
        B = BBox(((5, 10), (15, 25)))
        P = (16, 4)
        assert not (B.PointInside(P))

    def testLowerLeft(self):
        B = BBox(((5, 10), (15, 25)))
        P = (-10, 5)
        assert not (B.PointInside(P))

    def testBelow(self):
        B = BBox(((5, 10), (15, 25)))
        P = (10, 5)
        assert not (B.PointInside(P))

    def testAbove(self):
        B = BBox(((5, 10), (15, 25)))
        P = (10, 25.001)
        assert not (B.PointInside(P))

    def testLeft(self):
        B = BBox(((5, 10), (15, 25)))
        P = (4, 12)
        assert not (B.PointInside(P))

    def testRight(self):
        B = BBox(((5, 10), (15, 25)))
        P = (17.1, 12.3)
        assert not (B.PointInside(P))

    def testPointOnTopLine(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        P = (3.0, 10.)
        assert (B.PointInside(P))

    def testPointLeftTopLine(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        P = (-3.0, 10.)
        assert not (B.PointInside(P))

    def testPointOnBottomLine(self):
        B = BBox(((1.0, 2.0), (5., 10.)))
        P = (3.0, 5.)
        assert (B.PointInside(P))

    def testPointOnLeft(self):
        B = BBox(((-10., -10.), (-1.0, -1.0)))
        P = (-10, -5.)
        assert (B.PointInside(P))

    def testPointOnRight(self):
        B = BBox(((-10., -10.), (-1.0, -1.0)))
        P = (-1, -5.)
        assert (B.PointInside(P))

    def testPointOnBottomRight(self):
        B = BBox(((-10., -10.), (-1.0, -1.0)))
        P = (-1, -10.)
        assert (B.PointInside(P))


class Test_from_points():

    def testCreate(self):
        Pts = np.array(((5, 2), (3, 4), (1, 6)), np.float64)
        B = from_points(Pts)

        assert (B[0, 0] == 1.0 and
                B[0, 1] == 2.0 and
                B[1, 0] == 5.0 and
                B[1, 1] == 6.0)

    def testCreateInts(self):
        Pts = np.array(((5, 2), (3, 4), (1, 6)))
        B = from_points(Pts)
        assert (B[0, 0] == 1.0 and
                B[0, 1] == 2.0 and
                B[1, 0] == 5.0 and
                B[1, 1] == 6.0)

    def testSinglePoint(self):
        Pts = np.array((5, 2), np.float64)
        B = from_points(Pts)
        assert (B[0, 0] == 5. and
                B[0, 1] == 2.0 and
                B[1, 0] == 5. and
                B[1, 1] == 2.0)

    def testListTuples(self):
        Pts = [(3, 6.5), (13, 43.2), (-4.32, -4), (65, -23), (-0.0001, 23.432)]
        B = from_points(Pts)
        assert (B[0, 0] == -4.32
                and B[0, 1] == -23.0
                and B[1, 0] == 65.0
                and B[1, 1] == 43.2)


class TestMerge():

    A = BBox(((-23.5, 456), (56, 532.0)))
    B = BBox(((-20.3, 460), (54, 465)))   # B should be completely inside A
    C = BBox(((-23.5, 456), (58, 540.)))  # up and to the right or A
    D = BBox(((-26.5, 12), (56, 532.0)))

    def testInside(self):
        C = self.A.copy()
        C.Merge(self.B)
        assert (C == self.A)

    def testFullOutside(self):
        C = self.B.copy()
        C.Merge(self.A)
        assert (C == self.A)

    def testUpRight(self):
        A = self.A.copy()
        A.Merge(self.C)
        assert (A[0] == self.A[0] and A[1] == self.C[1])

    def testDownLeft(self):
        A = self.A.copy()
        A.Merge(self.D)
        assert (A[0] == self.D[0] and A[1] == self.A[1])


class TestWidthHeight():

    B = BBox(((1.0, 2.0), (5., 10.)))

    def testWidth(self):
        assert (self.B.Width == 4.0)

    def testWidth2(self):
        assert (self.B.Height == 8.0)

    def testSetW(self):
        with pytest.raises(AttributeError):
            self.B.Height = 6

    def testSetH(self):
        with pytest.raises(AttributeError):
            self.B.Width = 6


class TestCenter():

    B = BBox(((1.0, 2.0), (5., 10.)))

    def testCenter(self):
        assert ((self.B.Center == (3.0, 6.0)).all())

    def testSetCenter(self):
        with pytest.raises(AttributeError):
            self.B.Center = (6, 5)


class TestBBarray():

    BBarray = np.array((((-23.5, 456), (56, 532.0)), ((-20.3, 460),
                       (54, 465)), ((-23.5, 456), (58, 540.)), ((-26.5,
                       12), (56, 532.0))), dtype=np.float64)
    BB = asBBox(((-26.5, 12.), (58., 540.)))

    def testJoin(self):
        BB = fromBBArray(self.BBarray)
        assert BB == self.BB


class TestNullBBox():

    B1 = NullBBox()
    B2 = NullBBox()
    B3 = BBox(((1.0, 2.0), (5., 10.)))

    def testValues(self):
        assert (np.all(np.isnan(self.B1)))

    def testIsNull(self):
        assert (self.B1.IsNull)

    def testEquals(self):
        assert ((self.B1 == self.B2) is True)

    def testNotEquals(self):
        assert not self.B1 == self.B3

    def testNotEquals2(self):
        assert not self.B3 == self.B1

    def testMerge(self):
        C = self.B1.copy()
        C.Merge(self.B3)
        assert C == self.B3, 'merge failed, got: %s' % C

    def testOverlaps(self):
        assert self.B1.Overlaps(self.B3) is False

    def testOverlaps2(self):
        assert self.B3.Overlaps(self.B1) is False


class TestInfBBox():

    B1 = InfBBox()
    B2 = InfBBox()
    B3 = BBox(((1.0, 2.0), (5., 10.)))
    NB = NullBBox()

    def testValues(self):
        assert (np.all(np.isinf(self.B1)))

#    def testIsNull(self):
#        assert ( self.B1.IsNull )

    def testEquals(self):
        assert self.B1 == self.B2

    def testNotEquals(self):
        assert not self.B1 == self.B3

    def testNotEquals2(self):
        assert self.B1 != self.B3

    def testNotEquals3(self):
        assert not self.B3 == self.B1

    def testMerge(self):
        C = self.B1.copy()
        C.Merge(self.B3)
        assert C == self.B2, 'merge failed, got: %s' % C

    def testMerge2(self):
        C = self.B3.copy()
        C.Merge(self.B1)
        assert C == self.B1, 'merge failed, got: %s' % C

    def testOverlaps(self):
        assert (self.B1.Overlaps(self.B2) is True)

    def testOverlaps2(self):
        assert (self.B3.Overlaps(self.B1) is True)

    def testOverlaps3(self):
        assert (self.B1.Overlaps(self.B3) is True)

    def testOverlaps4(self):
        assert (self.B1.Overlaps(self.NB) is True)

    def testOverlaps5(self):
        assert (self.NB.Overlaps(self.B1) is True)


class TestSides():

    B = BBox(((1.0, 2.0), (5., 10.)))

    def testLeft(self):
        assert self.B.Left == 1.0

    def testRight(self):
        assert self.B.Right == 5.0

    def testBottom(self):
        assert self.B.Bottom == 2.0

    def testTop(self):
        assert self.B.Top == 10.0


class TestAsPoly():

    B = BBox(((5, 0), (10, 20)))
    corners = np.array([(5., 0.), (5., 20.), (10., 20.), (10., 0.)],
                       dtype=np.float64)

    def testCorners(self):
        print(self.B.AsPoly())
        assert np.array_equal(self.B.AsPoly(), self.corners)
