import numpy as np
import scipy


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
        self.principal_quantum=principal_quantum
        self.azimuthal_quantum=azimuthal_quantum
        self.magnetic_quantum=magnetic_quantum
        self.config = config
        self.r_norm = potential.r / (
            principal_quantum * config.a0
        )  # Normalize r for the excited state
        self.theta = np.arctan2(
            config.Y - potential.y_center, config.X - potential.x_center
        )
        # phi = np.zeros_like(theta)  # Azimuthal angle (0 for simplicity)
        self.phi = self.theta
        self.Ylm = scipy.special.sph_harm(
            magnetic_quantum, azimuthal_quantum, self.theta, self.phi
        )  # Spherical harmonic
        self.psi = (
            (2 / (principal_quantum * config.a0) ** (3 / 2))
            * self.r_norm
            * np.exp(-self.r_norm)
            * self.Ylm
        )
        integ = np.sum((abs(self.psi)**2)*(config.dx)*(config.dy))
        self.psi/=integ**(1/2)

    def propagate(self, V):
        """
        propagate the wave function in a potential field

        Attributes:
            np.array V: the potential field as an array
                of shape (Nx, Ny)
        """
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
