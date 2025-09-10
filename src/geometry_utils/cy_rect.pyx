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
