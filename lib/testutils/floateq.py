import lib


def floateq(x, y=0.0, tol=lib.TEST_TOLERANCE_TRESHOLD):
    return abs(y - x) < tol
