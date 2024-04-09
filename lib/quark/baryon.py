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
        super().__init__(
            config,
            [
                lib.quark.quark.Quark(
                    config, x0 - spread, y0, lib.quark.color.COLOR.RED
                ),
                lib.quark.quark.Quark(
                    config,
                    x0 + spread / 2,
                    y0 - spread / 2 * math.sqrt(3),
                    lib.quark.color.COLOR.GREEN,
                ),
                lib.quark.quark.Quark(
                    config,
                    x0 + spread / 2,
                    y0 + spread / 2 * math.sqrt(3),
                    lib.quark.color.COLOR.BLUE,
                ),
            ],
        )
        self.spread = spread
        self._meson = None
        self._cycle = 0
        self.T = 9

        self.colors = lib.quark.color.colorquarks(self.config, self.quarks)

    def propagate(self, V, particles, frame):
        particles = particles[:]
        super().propagate(V, particles, frame)
        if not (self.config.interactions_enabled):
            return

        if ((frame * self.config.dt) % self.T > 0) and self._cycle == 0:
            self._cycle = 1
            m = lib.quark.meson.Meson(
                self.config,
                self.quarks[0].x_center,
                self.quarks[0].y_center,
                self.spread * math.sqrt(3),
                -self.spread,
                2,
                lib.quark.color.COLOR.ANTIGREEN,
                lib.quark.color.COLOR.RED,
            )
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[0].color_charge = lib.quark.color.COLOR.GREEN
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        if ((frame * self.config.dt) % self.T > 1) and self._cycle == 1:
            self._cycle = 2
            for n in range(len(particles)):
                if particles[n]._id == self._meson:
                    del particles[n]
                    break
            self.quarks[1].color_charge = lib.quark.color.COLOR.RED
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        if ((frame * self.config.dt) % self.T > 3) and self._cycle == 2:
            self._cycle = 3
            m = lib.quark.meson.Meson(
                self.config,
                self.quarks[1].x_center,
                self.quarks[1].y_center,
                0,
                self.spread * 2,
                2,
                lib.quark.color.COLOR.ANTIBLUE,
                lib.quark.color.COLOR.RED,
            )
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[1].color_charge = lib.quark.color.COLOR.BLUE
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        if ((frame * self.config.dt) % self.T > 4) and self._cycle == 3:
            self._cycle = 4
            for n in range(len(particles)):
                if particles[n]._id == self._meson:
                    del particles[n]
                    break
            self.quarks[2].color_charge = lib.quark.color.COLOR.RED
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        if ((frame * self.config.dt) % self.T > 6) and self._cycle == 4:
            self._cycle = 5
            m = lib.quark.meson.Meson(
                self.config,
                self.quarks[2].x_center,
                self.quarks[2].y_center,
                -self.spread * math.sqrt(3),
                -self.spread,
                2,
                lib.quark.color.COLOR.ANTIGREEN,
                lib.quark.color.COLOR.RED,
            )
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[2].color_charge = lib.quark.color.COLOR.GREEN
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        if ((frame * self.config.dt) % self.T > 7) and self._cycle == 5:
            self._cycle = 0
            for n in range(len(particles)):
                if particles[n]._id == self._meson:
                    del particles[n]
                    break
            self.quarks[0].color_charge = lib.quark.color.COLOR.RED
            self.colors = lib.quark.color.colorquarks(self.config, self.quarks)
        return particles
