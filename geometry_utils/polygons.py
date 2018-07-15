"""
Polygon module, part of the geometry package

Assorted stuff for working with polygons

FIXME: should this support polygons with holes??? (i.e multiple rings?)

"""

import copy

import numpy as np

import BBox


class Polygon(np.ndarray):
    """
    A Polygon class

    This is a subclass of np.ndarray, so that it can be used in place of a
    simple array of points, but also can hold extra meta-data in a "metadata"
    dict.

    """
    def __new__(Polygon, points, metadata=None, copy=True, dtype=np.float):
        # fixme: this needs a better way to index and loop to get a point
        """
        Takes Points as an array. Data is any python sequence that can be
        turned into a Nx2 numpy array of floats. The data will be copied unless
        the copy argument is set to False.

        metadata is a dict of meta-data. This can hold anything.

        """
        # convert to array, copying data unless not requested.
        arr = np.array(points, dtype, copy=copy)
        arr.shape = (-1, 2)     # assure it's the right shape
        # Transform to a Polygon
        arr = arr.view(Polygon)
        # add the attribute
        # Use the specified 'metadata' parameter if given
        if metadata is not None:
            arr.metadata = metadata
        # Otherwise, use points metadata attribute if it exists
        else:
            arr.metadata = getattr(points, 'metadata', {})

        return arr

    def __array_finalize__(self, obj):
        '''
            ndarray subclass instances can come about in three ways:

            - explicit constructor call. This will call the usual sequence
              of SubClass.__new__ then (if it exists) SubClass.__init__.
            - View casting (e.g arr.view(SubClass))
            - Creating new from template (e.g. arr[:3])

            SubClass.__array_finalize__ gets called for all three methods
            of object creation, so this is where our object creation
            housekeeping usually goes.

            I got this from:
              http://www.scipy.org/Subclasses

                which has been deprecated and changed to...

              http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
        '''
        if obj is None:
            return

        self.metadata = getattr(obj, 'metadata', {})

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def __getitem__(self, index):
        """
        Override __getitem__ to return a ndarray, rather than a
        Polygon object
        """
        if type(index) is slice:
            return Polygon(np.ndarray.__getitem__(self, index), self.metadata)
        return np.asarray(np.ndarray.__getitem__(self, index))

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            # a Polygon is never equal to anything else
            return False
        else:
            return (np.array_equal(self, other) and
                    (self.metadata == other.metadata))

    def __ne__(self, other):
        return False if self == other else True

    def __str__(self):
        return ("Polygon with %i points.\nmetadata: %s" %
                (self.shape[0], self.metadata))

    def __repr__(self):
        msg = ["Polygon( [", ]
        pstr = []
        for point in self:
            try:
                pstr.append("[%s, %s]" % (point[0], point[1]))
            except IndexError:
                pass
        msg.append(",\n          ".join(pstr))
        msg.append("],\n         metadata=%s\n       )" % repr(self.metadata))
        return "".join(msg)

    @property
    def points(self):
        """
        the points as a regular np.ndarray
        """
        return np.asarray(self)

    @property
    def bounding_box(self):
        return BBox.fromPoints(self)

    @staticmethod
    def _scaling_fun(arr, scale):
        """
        scales and rounds -- does it all in place.
        """
        arr *= scale
        np.round(arr, out=arr)
        return arr

    def thin(self, scale):
        """
        Returns a new Polygon object, with the points thinned.

        :param scale: The scale to use: it is the ratio of world coords
                      (usually lat-lon degrees) to pixels.
        :type scale: (x_scale, y_scale): tuple of floats

        This is an algorithm designed for rendering. What it does
        is scale the points as you would to draw them (integer pixels).
        Then it removes any sequential duplicate points. Thus the rendered
        results should be exactly the same as if you rendered the pre-thinned
        polygons.

        Polygons that are reduced to 1 point are removed.

        If the polygon has teh first and last point the same, that property
        is preserved

        NOTE: in a sequence of close points, the first point is retained.
              Perhaps it would be better for the mean location of the
              sequence to be used instead? It should make no difference
              for rendering, but could make a difference for other purposes
        """
        scale = np.asarray(scale, dtype=np.float64)

        orig_poly = self
        sc_poly = self._scaling_fun(np.array(self), scale)
        prev_point = np.asarray(sc_poly[0])
        # special_case if last point matches first point
        last_same = 1 if np.array_equal(orig_poly[0], orig_poly[-1]) else 0
        thinned = [orig_poly[0]]
        for j in xrange(len(sc_poly)-last_same):
            point = sc_poly[j]
            if not np.array_equal(point, prev_point):
                thinned.append(orig_poly[j])
            prev_point = point
        if len(thinned) > 1:
            if last_same:
                thinned.append(orig_poly[0])
            return Polygon(thinned, metadata=orig_poly.metadata)
        else:
            return Polygon((), metadata=orig_poly.metadata)

def test():
    #  a test function

    p1 = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    p2 = p1 * 5

    set_ = PolygonSet()
    set_.append(p1)
    set_.append(p2)

    print set_[0]
    print set_[1]

    print "minimum is: ", set_.GetBoundingBox()[0]
    print "maximum is: ", set_.GetBoundingBox()[1]


if __name__ == "__main__":
    # run a test function
    test()
