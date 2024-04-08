import numpy as np
import math

import lib.quark.hadron
import lib.quark.color


class Meson(lib.quark.hadron.Hadron):
    """
    Now, I know gluons can have more than two quarks and
    what we are simulating here is not even a meson, let
    alone if it's the right particle for its job.

    Like I said, please send a pull request or issue
    if you know how to help us.

    """

    def __init__(self,
                 config,
                 x0: float,
                 y0: float,
                 vx: float,
                 vy: float,
                 spread: float,
                 c1: lib.quark.color.COLOR,
                 c2: lib.quark.color.COLOR):
        k = vy/vx
        ku = -1/k
        xa = 1
        ya = xa * ku
        u = math.sqrt(xa**2+ya**2)
        xa /= u
        ya /= u
        super().__init__(config, [
            lib.quark.quark.Quark(config, x0 + xa*spread, y0 + ya*spread, c1),
            lib.quark.quark.Quark(config, x0 - xa*spread, y0 - ya*spread, c2),
        ])

        R = 0 * math.pi / 3
        G = 2 * math.pi / 3
        B = 4 * math.pi / 3
        for x in range(config.Nx):
            for y in range(config.Ny):
                x_norm = x - config.Nx / 2
                y_norm = y - config.Ny / 2
                theta = np.angle(x_norm + 1j * y_norm)
                theta += math.pi
                r = max(1 - abs(R - theta) ** 4, 1 -
                        abs(R+2*math.pi - theta) ** 4, 0)
                g = max(1 - abs(G - theta) ** 4, 1 -
                        abs(G+2*math.pi - theta) ** 4, 0)
                b = max(1 - abs(B - theta) ** 4, 1 -
                        abs(B+2*math.pi - theta) ** 4, 0)
                self.colors[x][y] = np.array((r, g, b))

    def propagate(self, V, particles, frame):
        super().propagate(V, particles, frame)
