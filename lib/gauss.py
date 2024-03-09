import numpy as np


class WavePacket:
    """
    Gaussian wave packet.
    Pretty simple representation of a photon or other alone particle

    Attributes:
        float sigma: the uncertainty in the initial position
        float kx0: initial width of the wave packet
        float ky0: initial height of the wave packet
        float x0: initial x position
        float y0: initial y position
    """

    def __init__(
        self,
        config,
        sigma=0.5,
        kx0=2.0,
        ky0=2.0,
        x0=2.0,
        y0=5.0,
    ):
        self.config = config
        self.psi = np.exp(
            -((config.X - x0) ** 2 + (config.Y - y0) ** 2) / (2 * sigma**2)
        ) * np.exp(1j * (kx0 * config.X + ky0 * config.Y))

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