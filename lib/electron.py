import numpy as np
import scipy
import uuid
import random

import lib


class Electron:
    """
    Basic representation of an electron in an atom.

    Attributes:
        Config config: experiment configurations
        Potential potential: the potential field
            we are modeling the electron in
        int principal_quantum: principal quantum number
            (aka energy level or electron orbital)
        int azimuthal_quantum: azimuthal quantum number
            (aka suborbital)
        int magnetic_quantum: magnetic quantum number
            (experimental, better leave it at default)
    """

    def __init__(
        self,
        config,
        potential,
        principal_quantum=1,
        azimuthal_quantum=0,
        magnetic_quantum=0,
    ):
        self._id = uuid.uuid4()
        self.principal_quantum = principal_quantum
        self.azimuthal_quantum = azimuthal_quantum
        self.magnetic_quantum = magnetic_quantum
        self.config = config
        self.psi = self.calculate_psi(potential)
        integ = np.sum((abs(self.psi) ** 2) * (config.dx) * (config.dy))
        self.psi /= integ ** (1 / 2)

    def calculate_psi(self, potential):
        '''
        calculate the wave function for a bound electron with given n, l, m
        '''
        r_norm = potential.r / (
            self.principal_quantum * self.config.a0
        )  # Normalize r for the excited state
        theta = np.arctan2(
            self.config.Y - potential.y_center,
            self.config.X - potential.x_center
        )
        # phi = np.zeros_like(theta)  # Azimuthal angle (0 for simplicity)
        phi = theta
        Ylm = scipy.special.sph_harm(
            self.magnetic_quantum, self.azimuthal_quantum, theta, phi
        )  # Spherical harmonic
        psi = (
            (2 / (self.principal_quantum * self.config.a0) ** (3 / 2))
            * r_norm
            * np.exp(-r_norm)
            * Ylm
        )
        return psi

    def propagate(self, V, particles):
        """
        propagate the wave function in a potential field

        Attributes:
            np.array V: the potential field as an array
                of shape (Nx, Ny)
        """

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

        if self.principal_quantum > 1:
            pass
            # emit photons
