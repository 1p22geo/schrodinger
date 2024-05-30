import numpy as np
import math


class COLOR:
    RED = "COLOR.RED"
    BLUE = "COLOR.BLUE"
    GREEN = "COLOR.GREEN"
    ANTIRED = "COLOR.ANTIRED"
    ANTIBLUE = "COLOR.ANTIBLUE"
    ANTIGREEN = "COLOR.ANTIGREEN"

    def ANTI(c):
        match c:
            case COLOR.RED:
                return COLOR.ANTIRED
            case COLOR.GREEN:
                return COLOR.ANTIGREEN
            case COLOR.BLUE:
                return COLOR.ANTIBLUE
            case COLOR.ANTIRED:
                return COLOR.RED
            case COLOR.ANTIGREEN:
                return COLOR.GREEN
            case COLOR.ANTIBLUE:
                return COLOR.BLUE


def colorquarks(config, quarks):
    """
    Returns a `np.array` of shape (Nx, Ny, 3)
    where each point is asigned its "color"
    for matplotlib graphing based on the array
    of quarks
    """
    colors = np.zeros((config.Nx, config.Ny, 3))
    for x in range(config.Nx):
        for y in range(config.Ny):
            for q in quarks:
                x0 = q.x_center / config.dx
                y0 = q.y_center / config.dy
                d = math.sqrt((x - x0) ** 2 + (y - y0) ** 2)
                f = min(max(0, (200 - d) / 200), 1)
                match q.color_charge:
                    case COLOR.RED:
                        colors[x][y] += np.array((f, 0, 0))
                    case COLOR.GREEN:
                        colors[x][y] += np.array((0, f, 0))
                    case COLOR.BLUE:
                        colors[x][y] += np.array((0, 0, f))
                    case COLOR.ANTIRED:
                        colors[x][y] += np.array((0, f, f))
                    case COLOR.ANTIGREEN:
                        colors[x][y] += np.array((f, 0, f))
                    case COLOR.ANTIBLUE:
                        colors[x][y] += np.array((f, f, 0))
            colors[x][y] = [sorted((0, c, 1))[1] for c in colors[x][y]]

    return colors


def rotate(color, n=0):
    """
    Rotates the color `n` times in the order:

    > RED -> GREEN -> BLUE -> RED -> GREEN -> ...

    or

    > ~RED -> ~GREEN -> ~BLUE -> ~RED -> ...

    (where ~RED is ANTIRED)
    """
    if not n:
        return color
    match color:
        case COLOR.RED:
            return rotate(COLOR.GREEN, n-1)
        case COLOR.GREEN:
            return rotate(COLOR.BLUE, n-1)
        case COLOR.BLUE:
            return rotate(COLOR.RED, n-1)
        case COLOR.ANTIRED:
            return rotate(COLOR.ANTIGREEN, n-1)
        case COLOR.ANTIGREEN:
            return rotate(COLOR.ANTIBLUE, n-1)
        case COLOR.ANTIBLUE:
            return rotate(COLOR.ANTIRED, n-1)
