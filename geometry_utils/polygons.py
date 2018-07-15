import numpy

def polygon_inside(polygon_verts, trial_points):
    '''
    Return a Boolean array the size of the trial point array True if point is inside

    INPUTS
    ------
    polygon_verts:  Mx2 array
    trial_points:   Nx2 array

    RETURNS
    -------
    inside_points:  Boolean array (len(N))
                    True if the trial point is inside the polygon
    '''

    ## Code

    return inside

def polygon_area():

    return area

def polygon_issimple(polygon_verts):
    '''
    Return true if the polygon is simple
    '''

    # code

    return issimple

def polygon_rotation(polygon_verts):
    '''
    Return a unit vector, with sign associated with the sense of rotation

    INPUT
    -----
    polygon_verts:  Mx2 array

    OUTPUT
    ------
    rotation:  scalar
               A 'unit vector' with a sign associated with the rotation
               1 for a positive rotation according to the right-hand rule
              -1 for a negative rotation according to the right hand rule

              Note, only defined for a simple polygon. Raises error if not simple.
    '''

    # code

    return rotation

def polygon_centroid(polygon_verts):
    '''
    Return the (x, y) location of the polygon centroid

    INPUT
    -----
    polygon_verts:  Mx2 array

    OUTPUT
    ------
    xy_centroid:  1x2

    '''

    return xy
    