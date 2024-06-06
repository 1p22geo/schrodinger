import math

import libschrodinger.quark.hadron
import libschrodinger.quark.color
import libschrodinger.quark.meson
import libschrodinger.quark.quark


class Baryon(libschrodinger.quark.hadron.Hadron):
    """
    Equally abstract [and EXPERIMENTAL] class for baryons.

    But hey, colors! :3
    """

    rotation: int
    """
    How many times are the colors rotated

    Also see `libschrodinger.quark.color.rotate`
    """
    spread: float
    """
    How much should the quarks be spread out.

    The average distance between two quarks within a baryon
    """
    T: float
    """
    How much does one quark emission cycle take.

    Default is 9.0 meaning it takes 9.0 units of time for three gluons
    [`libschrodinger.quark.meson.Meson`] to be emmited and absorbed.
    """

    def __init__(
        self, config, x0: float, y0: float, spread: float = 3.0, rotation: int = 0
    ):
        self.rotation = rotation
        super().__init__(
            config,
            [
                libschrodinger.quark.quark.Quark(
                    config,
                    x0 - spread,
                    y0,
                    libschrodinger.quark.color.rotate(
                        libschrodinger.quark.color.COLOR.RED, self.rotation
                    ),
                ),
                libschrodinger.quark.quark.Quark(
                    config,
                    x0 + spread / 2,
                    y0 - spread / 2 * math.sqrt(3),
                    libschrodinger.quark.color.rotate(
                        libschrodinger.quark.color.COLOR.GREEN, self.rotation
                    ),
                ),
                libschrodinger.quark.quark.Quark(
                    config,
                    x0 + spread / 2,
                    y0 + spread / 2 * math.sqrt(3),
                    libschrodinger.quark.color.rotate(
                        libschrodinger.quark.color.COLOR.BLUE, self.rotation
                    ),
                ),
            ],
        )
        self.spread = spread
        self._meson = None
        self._cycle = 0
        self.T = 9

        self.colors = libschrodinger.quark.color.colorquarks(
            self.config, self.quarks)

    def propagate(self, V, particles, frame):
        super().propagate(V, particles, frame)
        if not (self.config.interactions_enabled):
            return

        if ((frame * self.config.dt) % self.T > 0) and self._cycle == 0:
            self._cycle = 1
            m = libschrodinger.quark.meson.Meson(
                self.config,
                self.quarks[0].x_center,
                self.quarks[0].y_center,
                self.spread * math.sqrt(3),
                -self.spread,
                2,
                libschrodinger.quark.color.rotate(
                    libschrodinger.quark.color.COLOR.ANTIGREEN, self.rotation
                ),
                libschrodinger.quark.color.rotate(
                    libschrodinger.quark.color.COLOR.RED, self.rotation
                ),
            )
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[0].color_charge = libschrodinger.quark.color.rotate(
                libschrodinger.quark.color.COLOR.GREEN, self.rotation
            )
            self.colors = libschrodinger.quark.color.colorquarks(
                self.config, self.quarks
            )
        if ((frame * self.config.dt) % self.T > 1) and self._cycle == 1:
            self._cycle = 2
            for n in range(len(particles)):
                if particles[n]._id == self._meson:
                    del particles[n]
                    break
            self.quarks[1].color_charge = libschrodinger.quark.color.rotate(
                libschrodinger.quark.color.COLOR.RED, self.rotation
            )
            self.colors = libschrodinger.quark.color.colorquarks(
                self.config, self.quarks
            )
        if ((frame * self.config.dt) % self.T > 3) and self._cycle == 2:
            self._cycle = 3
            m = libschrodinger.quark.meson.Meson(
                self.config,
                self.quarks[1].x_center,
                self.quarks[1].y_center,
                0,
                self.spread * 2,
                2,
                libschrodinger.quark.color.rotate(
                    libschrodinger.quark.color.COLOR.ANTIBLUE, self.rotation
                ),
                libschrodinger.quark.color.rotate(
                    libschrodinger.quark.color.COLOR.RED, self.rotation
                ),
            )
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[1].color_charge = libschrodinger.quark.color.rotate(
                libschrodinger.quark.color.COLOR.BLUE, self.rotation
            )
            self.colors = libschrodinger.quark.color.colorquarks(
                self.config, self.quarks
            )
        if ((frame * self.config.dt) % self.T > 4) and self._cycle == 3:
            self._cycle = 4
            for n in range(len(particles)):
                if particles[n]._id == self._meson:
                    del particles[n]
                    break
            self.quarks[2].color_charge = libschrodinger.quark.color.rotate(
                libschrodinger.quark.color.COLOR.RED, self.rotation
            )
            self.colors = libschrodinger.quark.color.colorquarks(
                self.config, self.quarks
            )
        if ((frame * self.config.dt) % self.T > 6) and self._cycle == 4:
            self._cycle = 5
            m = libschrodinger.quark.meson.Meson(
                self.config,
                self.quarks[2].x_center,
                self.quarks[2].y_center,
                -self.spread * math.sqrt(3),
                -self.spread,
                2,
                libschrodinger.quark.color.rotate(
                    libschrodinger.quark.color.COLOR.ANTIGREEN, self.rotation
                ),
                libschrodinger.quark.color.rotate(
                    libschrodinger.quark.color.COLOR.RED, self.rotation
                ),
            )
            particles.append(m)
            self._meson = m._id  # to access or delete this meson later on
            self.quarks[2].color_charge = libschrodinger.quark.color.rotate(
                libschrodinger.quark.color.COLOR.GREEN, self.rotation
            )
            self.colors = libschrodinger.quark.color.colorquarks(
                self.config, self.quarks
            )
        if ((frame * self.config.dt) % self.T > 7) and self._cycle == 5:
            self._cycle = 0
            for n in range(len(particles)):
                if particles[n]._id == self._meson:
                    del particles[n]
                    break
            self.quarks[0].color_charge = libschrodinger.quark.color.rotate(
                libschrodinger.quark.color.COLOR.RED, self.rotation
            )
            self.colors = libschrodinger.quark.color.colorquarks(
                self.config, self.quarks
            )
        return particles
