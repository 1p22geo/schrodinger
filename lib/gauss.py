import numpy as np
import uuid

import lib.particle
import lib.waveutils
import lib.config


class WavePacket(lib.particle.Particle):
    """
    Gaussian wave packet.
    Pretty simple representation of a photon or other alone particle
    """

    sigma: float
    """
    the uncertainty of the initial position
    """
    kx0: float
    """
    initial width for the wave packet
    """
    ky0: float
    """
    initial height for the wave packet
    """
    x0: float
    """
    initial X position for the wave packet
    """
    y0: float
    """
    initial Y position for the wave packet
    """
    vx: float
    """
    X component for the velocity [EXPERIMENTAL]
    """
    vy: float
    """
    Y component for the velocity [EXPERIMENTAL]
    """
    config: lib.config.Config
    """
    configuration for the domain
    """
    psi: np.array
    """
    the wave function  

    a `np.array` of shape `(config.Nx, config.Ny)`
    """

    def __init__(
        self,
        config,
        sigma=0.5,
        kx0=2.0,
        ky0=2.0,
        x0=2.0,
        y0=5.0,
        vx=0.0,
        vy=0.0,
    ):
        self._id = uuid.uuid4()
        self.config = config
        self.vx = vx
        self.vy = vy
        self.psi = np.exp(
            -((config.X - x0) ** 2 + (config.Y - y0) ** 2) / (2 * sigma**2)
        ) * np.exp(1j * (kx0 * config.X + ky0 * config.Y))

        integ = np.sum((abs(self.psi) ** 2) * (config.dx) * (config.dy))
        self.psi /= integ ** (1 / 2)

    def propagate(self, V: np.array, particles: list[lib.particle.Particle]):
        """
        propagate the wave function in a potential field

        Parameters:
        - `np.array V`: the potential field as an array
            of shape (Nx, Ny)
        - `Particle[] particles`: an array of other particles
            for inter-particle interactions

        """

        self.psi = lib.waveutils.rollwave(self.config, self.psi, self.vx, self.vy)

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

        if not (self.config.interactions_enabled):
            return
        # Interact with other particles
        for p in particles:
            if p._id == self._id:
                continue
            pass
            # interact with particle
