import lib.constants as constants


def floateq(x, y=0.0, tol=constants.TEST_TOLERANCE_TRESHOLD):
    """
    Checks if `x == y` with a tolerance of `tol`
    """
    return abs(y - x) < tol
