import numpy as np
import math

import lib.quark.hadron
import lib.quark.color
import lib.quark.meson


class Baryon(lib.quark.hadron.Hadron):
    """
    Equally abstract [and EXPERIMENTAL] class for baryons.

    But hey, colors! :3
    """

    def __init__(self, config, x0: float, y0: float, spread: float):
        super().__init__(config, [
            lib.quark.quark.Quark(config, x0-spread, y0,
                                  lib.quark.color.COLOR.RED),
            lib.quark.quark.Quark(config, x0 + spread/2,
                                  y0-spread/2*math.sqrt(3),
                                  lib.quark.color.COLOR.GREEN),
            lib.quark.quark.Quark(config, x0 + spread/2,
                                  y0+spread/2*math.sqrt(3),
                                  lib.quark.color.COLOR.BLUE)
        ])
        self.spread = spread
        self._meson = None

        self.colors = lib.quark.color.colorquarks(self.config, self.quarks)

    def propagate(self, V, particles, frame):
        super().propagate(V, particles, frame)
        if not (self.config.interactions_enabled):
            return

        if frame % 150 == 1:
            m = lib.quark.meson.Meson(
                self.config,
                self.quarks[0].x_center,
                self.quarks[0].y_center,
                self.spread,
                -self.spread*math.sqrt(3),
                2,
                lib.quark.color.COLOR.ANTIGREEN,
                lib.quark.color.COLOR.RED)
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[0].color_charge = lib.quark.color.COLOR.GREEN
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        return particles
