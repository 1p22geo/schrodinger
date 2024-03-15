import numpy as np


class Potential:
    def __init__(self, config, x_center=None, y_center=None):
        self.x_center = x_center if x_center else config.Lx / 2
        self.y_center = y_center if y_center else config.Ly / 2
        self.r = np.sqrt(
            (config.X - self.x_center) ** 2 + (config.Y - self.y_center) ** 2
        )
        self.V = np.zeros((config.Nx, config.Ny))
        self.V[:, :] = 0


class CoulombPotential(Potential):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.V = -1 / self.r  # Central Coulomb potential


class MeanFieldPotential(Potential):
    def __init__(self, config, particle, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.rho = np.abs(particle.psi) ** 2  # Charge density of electron
        self.V = -1 / np.sqrt(
            (config.X - self.x_center) ** 2 + (config.Y - self.y_center) ** 2 + 1e-6
        )  # Regularize the denominator
        self.V *= np.sum(self.rho) * config.dx * config.dy  # Scale by charge
