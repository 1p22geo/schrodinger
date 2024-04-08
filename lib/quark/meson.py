import numpy as np
import math

import lib.quark.hadron
import lib.quark.color

import lib.waveutils


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
        self.vx = vx
        self.vy = vy
        self.x0 = x0
        self.y0 = y0
        super().__init__(config, [
            lib.quark.quark.Quark(config, x0 + xa*spread, y0 + ya*spread, c1),
            lib.quark.quark.Quark(config, x0 - xa*spread, y0 - ya*spread, c2),
        ])
        self.colors = lib.quark.color.colorquarks(self.config, self.quarks)

    def propagate(self, V, particles, frame):
        for n in range(len(self.quarks)):
            self.quarks[n].psi = lib.waveutils.rollwave(
                self.config, self.quarks[n].psi, self.vx, self.vy)
            self.quarks[n].x_center += self.vx * self.config.dt
            self.quarks[n].y_center += self.vy * self.config.dt

        super().propagate(V, particles, frame)
        self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
