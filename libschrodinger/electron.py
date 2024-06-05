import numpy as np
import scipy
import uuid

import libschrodinger.particle
import libschrodinger.config
import libschrodinger.potential
import libschrodinger.gauss


class Electron(libschrodinger.particle.Particle):
    """
    Basic representation of an electron in an atom.
    """

    config: libschrodinger.config.Config
    """
       experiment configurations
    """
    potential: libschrodinger.potential.Potential
    """
    the potential field
            we are modeling the electron in
    """
    principal_quantum: int
    """
    principal quantum number
            (aka energy level or electron orbital)
    """
    azimuthal_quantum: int
    """
    azimuthal quantum number
            (aka suborbital)
    """
    magnetic_quantum: int
    """
    magnetic quantum number
            (experimental, better leave it at default)
    """
    psi: np.ndarray
    """
    the wave function  

    a `np.array` of shape `(config.Nx, config.Ny)`
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
        self.potential = potential

        self._photon = None
        self._cycle = 0
        self.T = 5

        self.psi = self.calculate_psi(potential)
        integ = np.sum((abs(self.psi) ** 2) * (config.dx) * (config.dy))
        self.psi /= integ ** (1 / 2)

    def calculate_psi(self, potential: libschrodinger.potential.Potential):
        """
        Calculate the wave function for a bound electron with given n, l, m

        Parameters
        ----------
        - potential: libschrodinger.potential.Potential
            - the actual potential function to model an electron in
        """
        r_norm = potential.r / (
            self.principal_quantum * self.config.a0
        )  # Normalize r for the excited state
        theta = np.arctan2(
            self.config.Y - potential.y_center, self.config.X - potential.x_center
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

    def propagate(
        self, V: np.ndarray, particles: list[libschrodinger.particle.Particle], frame: int
    ):
        """
        propagate the wave function in a potential field

        Parameters
        ----------
        - `V: np.ndarray`
            - the potential field as an array
            of shape (Nx, Ny)
        - `particles: list[libschrodinger.particle.Particle]`
            - an array of other particles
            for inter-particle interactions

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
        if (
            ((frame * self.config.dt) % self.T > 0)
            and ((frame * self.config.dt) % self.T < 1)
            and self._cycle == 0
        ):
            if self.principal_quantum < 2:
                # broke-ass electron, can't even afford a photon xd
                return
            self._cycle = 1
            p = libschrodinger.gauss.WavePacket(
                self.config,
                0.3,
                2,
                2,
                self.potential.x_center,
                self.potential.y_center,
                0,
                self.config.Ly,
                # The photon has to run 1 Ly in 1 dt of time
                # No, Ly is not light-year. It's the width of the simulation.
            )
            particles.append(p)
            self._photon = p._id
            self.principal_quantum -= 1
            self.psi = self.calculate_psi(self.potential)
            return particles
        if ((frame * self.config.dt) % self.T > 1) and self._cycle == 1:
            self._cycle = 0
            for n in range(len(particles)):
                if particles[n]._id == self._photon:
                    del particles[n]
                    break

            self.principal_quantum += 1
            self.psi = self.calculate_psi(self.potential)
            return particles
