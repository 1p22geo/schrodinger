import numpy as np
import math
import uuid

import lib.particle
import lib.config
import lib.potential


class Quark(lib.particle.Particle):
    """
    [HIGHLY EXPERIMENTAL]

    You see, every simulation has its limits of resemblance to real world.
    And our quantum simulation simulates only non-relativistic quantum physics.
    Quantum chromodynamics and lattice QCD is too difficult for us.

    But if you have the required knowledge, please do not hesistate and help us
        in whatever way you can.

    """

    config: lib.config.Config
    """
       experiment configurations
    """
    psi: np.array
    """
    the wave function

    a `np.array` of shape `(config.Nx, config.Ny)`
    """
    x_center: float
    """
    x0, midpoint of the wave function
    """
    y_center: float
    """
    y0, midpoint of the wave function
    """

    def __init__(self, config, x_center, y_center):
        self._id = uuid.uuid4()
        self.config = config
        self.x_center = x_center
        self.y_center = y_center
        self.psi = np.zeros((config.Nx, config.Ny), dtype="complex128")
        for x in range(config.Nx):
            for y in range(config.Ny):
                x_norm = x * config.dx - x_center
                y_norm = y * config.dy - y_center

                r = math.sqrt(x_norm**2 + y_norm**2)
                self.psi[x][y] = math.exp(-r / config.a0)

    def propagate(self, V: np.array, particles: list[lib.particle.Particle]):
        """
        propagate the wave function in a potential field

        Parameters
        ----------
        - `V: np.array`
            - the potential field as an array
            of shape (Nx, Ny)
        - `particles: list[lib.particle.Particle]`
            - an array of other particles
            for inter-particle interactions

        """

        # Quarks don't interact with electromagnetic fields in
        # a normal way, so I will just make them kinda sit in place.
        #
        # Once again, a major simplification.
        V = lib.potential.CoulombPotential(
            self.config, self.x_center, self.y_center).V

        # Propagate through the Schrodinger's equation
        self.psi = self.psi * np.exp(-1j * (V) * self.config.dt / 2)
        self.psi = np.fft.fft2(self.psi)
        self.psi = self.psi * np.exp(
            -1j
            * (
                np.fft.fftfreq(self.config.Nx, self.config.dx) ** 2
                + np.fft.fftfreq(self.config.Ny, self.config.dy) ** 2
            )
            * self.config.dt
        )
        self.psi = np.fft.ifft2(self.psi)
        self.psi = self.psi * np.exp(-1j * (V) * self.config.dt / 2)

        if not (self.config.interactions_enabled):
            return
        # Interact with other particles
        for p in particles:
            if p._id == self._id:
                continue
            pass
            # interact with particle
