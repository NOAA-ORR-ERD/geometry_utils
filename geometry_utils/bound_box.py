"""
A Bounding Box object and assorted utilities , subclassed from a numpy array

Also -- is this simple a rectangle class?

FIXME: The constructor functions should be class methods.
       It would be good to PEP8 the method names.

TODO:  Cythonizing this could speed things up -- which could be nice.
"""

import numpy as np


class BBox(np.ndarray):
    """
    A Bounding Box object:

    Takes Data as an array. Data is any python sequence that can be
    turned into a 2x2 numpy array of float64s:

    [[MinX, MinY ],
     [MaxX, MaxY ]]

    It is a subclass of numpy.ndarray, so for the most part it can be used
    as an array, and arrays that fit the above description can be used
    in its place.

    Usually created by the factory functions:

        asBBox

        and

        fromPoints
    """
    def __new__(subtype, data):
        """
        Takes Data as an array. Data is any python sequence that can be turned
        into a 2x2 numpy array of float64s:

        [[MinX, MinY ],
        [MaxX, MaxY ]]

        You don't usually call this directly. BBox objects are created with
        the factory functions:

        asBBox

        and

        from_points
        """
        arr = np.array(data, np.float64)
        arr.shape = (2, 2)

        if arr[0, 0] > arr[1, 0] or arr[0, 1] > arr[1, 1]:
            # note: zero sized BB OK.
            raise ValueError('BBox values not aligned:\n'
                             'minimum values must be less that maximum values')

        return np.ndarray.__new__(BBox, shape=arr.shape, dtype=arr.dtype,
                                  buffer=arr)

    def Overlaps(self, BB):
        """
        Overlap(BB):

        Tests if the given Bounding Box overlaps with this one.
        Returns True is the Bounding boxes overlap, False otherwise
        If they are just touching, returns True
        """

        if np.isinf(self).all() or np.isinf(BB).all():
            return True
        if ((self[1, 0] >= BB[0, 0]) and (self[0, 0] <= BB[1, 0]) and
                (self[1, 1] >= BB[0, 1]) and (self[0, 1] <= BB[1, 1])):
            return True
        else:
            return False

    def Inside(self, BB):
        """
        Inside(BB):

        Tests if the given Bounding Box is entirely inside this one.

        Returns True if it is entirely inside, or touching the
        border.

        Returns False otherwise
        """
        if ((BB[0, 0] >= self[0, 0]) and (BB[1, 0] <= self[1, 0]) and
                (BB[0, 1] >= self[0, 1]) and (BB[1, 1] <= self[1, 1])):
            return True
        else:
            return False

    def PointInside(self, Point):
        """
        Inside(BB):

        Tests if the given Point is entirely inside this one.

        Returns True if it is entirely inside, or touching the
        border.

        Returns False otherwise

        Point is any length-2 sequence (tuple, list, array) or two numbers
        """
        if (Point[0] >= self[0, 0] and
                Point[0] <= self[1, 0] and
                Point[1] <= self[1, 1] and
                Point[1] >= self[0, 1]):
            return True
        else:
            return False

    def Merge(self, BB):
        """
        Joins this bounding box with the one passed in, maybe making this one
        bigger
        """
        if self.IsNull():
            self[:] = BB
        elif np.isnan(BB).all():
            # BB may be a regular array, so I can't use IsNull
            pass
        else:
            if BB[0, 0] < self[0, 0]:
                self[0, 0] = BB[0, 0]
            if BB[0, 1] < self[0, 1]:
                self[0, 1] = BB[0, 1]
            if BB[1, 0] > self[1, 0]:
                self[1, 0] = BB[1, 0]
            if BB[1, 1] > self[1, 1]:
                self[1, 1] = BB[1, 1]

        return None

    def AsPoly(self):
        """
        Returns the four corners of the bounding box as polygon:

        An 4X2 array of (x,y) coordinates of the corners

        """
        return np.array(((self[0, 0], self[0, 1]),
                         (self[0, 0], self[1, 1]),
                         (self[1, 0], self[1, 1]),
                         (self[1, 0], self[0, 1]),
                         ), dtype=np.float64)

    def IsNull(self):
        return np.isnan(self).all()

    # fixme: it would be nice to add setter, too.
    def _getLeft(self):
        return self[0, 0]
    Left = property(_getLeft)

    def _getRight(self):
        return self[1, 0]
    Right = property(_getRight)

    def _getBottom(self):
        return self[0, 1]
    Bottom = property(_getBottom)

    def _getTop(self):
        return self[1, 1]
    Top = property(_getTop)

    def _getWidth(self):
        return self[1, 0] - self[0, 0]
    Width = property(_getWidth)

    def _getHeight(self):
        return self[1, 1] - self[0, 1]
    Height = property(_getHeight)

    def _getCenter(self):
        return self.sum(0) / 2.0
    Center = property(_getCenter)
    # This could be used for a make BB from a bunch of BBs

    # def _getboundingbox(bboxarray): # lrk: added this
    #    # returns the bounding box of a bunch of bounding boxes
    #    upperleft = np.minimum.reduce(bboxarray[:,0])
    #    lowerright = np.maximum.reduce(bboxarray[:,1])
    #    return np.array((upperleft, lowerright), np.float64)
    # _getboundingbox = staticmethod(_getboundingbox)

    # Save the ndarray __eq__ for internal use.
    Array__eq__ = np.ndarray.__eq__

    def __eq__(self, other):
        """
        __eq__(BB) The equality operator

        A == B if and only if all the entries are the same
        """
        if self.IsNull() and np.isnan(other).all():
            # BB may be a regular array, so I can't use IsNull
            return True
        else:
            return self.Array__eq__(other).all()

    def __ne__(self, other):

        return not self.__eq__(other)


def asBBox(data):
    """
    returns a BBox object.

    If object is a BBox, it is returned unaltered

    If object is a numpy array, a BBox object is returned that shares a
    view of the data with that array. The numpy array should be of the correct
    format: a 2x2 numpy array of float64s:

    [[MinX, MinY ],
     [MaxX, MaxY ]]
    """
    if isinstance(data, BBox):
        return data
    arr = np.asarray(data, np.float64)
    return np.ndarray.__new__(BBox, shape=arr.shape, dtype=arr.dtype,
                              buffer=arr)


def from_points(points):
    """
    from_points (points).

    reruns the bounding box of the set of points in points. points can
    be any python object that can be turned into a numpy NX2 array of float64s.

    If a single point is passed in, a zero-size Bounding Box is returned.
    """
    points = np.asarray(points, np.float64).reshape(-1, 2)

    arr = np.vstack((points.min(0), points.max(0)))

    return np.ndarray.__new__(BBox,
                              shape=arr.shape,
                              dtype=arr.dtype,
                              buffer=arr)


def fromBBArray(BBarray):
    """
    Builds a BBox object from an array of Bounding Boxes.
    The resulting Bounding Box encompases all the included BBs.

    The BBarray is in the shape: (Nx2x2) where BBarray[n] is a 2x2 array that
    represents a BBox
    """
    # upperleft = np.minimum.reduce(BBarray[:,0])
    # lowerright = np.maximum.reduce(BBarray[:,1])

    #   BBarray = np.asarray(BBarray, np.float64).reshape(-1,2)
    #   arr = np.vstack( (BBarray.min(0), BBarray.max(0)) )
    BBarray = np.asarray(BBarray, np.float64).reshape(-1, 2, 2)
    arr = np.vstack((BBarray[:, 0, :].min(0), BBarray[:, 1, :].max(0)))
    return asBBox(arr)
    # return asBBox( (upperleft, lowerright) ) * 2


def NullBBox():
    """
    Returns a BBox object with all NaN entries.

    This represents a Null BB box;

    BB merged with it will return BB.

    Nothing is inside it.
    """
    arr = np.array(((np.nan, np.nan), (np.nan, np.nan)), np.float64)
    return np.ndarray.__new__(BBox, shape=arr.shape, dtype=arr.dtype,
                              buffer=arr)


def InfBBox():
    """
    Returns a BBox object with all -inf and inf entries

    """
    arr = np.array(((-np.inf, -np.inf), (np.inf, np.inf)), np.float64)
    return np.ndarray.__new__(BBox, shape=arr.shape, dtype=arr.dtype,
                              buffer=arr)
