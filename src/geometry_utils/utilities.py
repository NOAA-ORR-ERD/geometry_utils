"""
Assorted small utilities used with the rest of the package

"""
import numpy as np

def point(x, y):
    """
    makes a compatible numpy array -- makes testing easier
    """
    return np.array((x, y), dtype=np.float64)

def vector(x, y):
    """
    A vector and a point are exactly the same:
    two values

    But it can be helpful to assign them different meaning
    """
    return np.array((x, y), dtype=np.float64)
