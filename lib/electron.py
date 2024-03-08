import numpy as np
import scipy


class Electron():
    def __init__(self, config, potential, n=1, l=0, m=0):
        self.config = config
        self.r_norm = potential.r / (n * config.a0)  # Normalize r for the excited state
        self.theta = np.arctan2(config.Y - potential.y_center, config.X - potential.x_center)
        # phi = np.zeros_like(theta)  # Azimuthal angle (0 for simplicity)
        self.phi = self.theta
        self.Ylm = scipy.special.sph_harm(m, l, self.theta, self.phi)  # Spherical harmonic
        self.psi = (2 / (n * config.a0)**(3/2)) * self.r_norm * np.exp(-self.r_norm) * self.Ylm
    
    def propagate(self, V):
        self.psi = self.psi * np.exp(-1j * (V) * self.config.dt / 2)
        self.psi = np.fft.fft2(self.psi)
        self.psi = self.psi * np.exp(-1j * (np.fft.fftfreq(self.config.Nx, self.config.dx)**2 + np.fft.fftfreq(self.config.Ny, self.config.dy)**2) * self.config.dt)
        self.psi = np.fft.ifft2(self.psi)
        self.psi = self.psi * np.exp(-1j * (V) * self.config.dt / 2)