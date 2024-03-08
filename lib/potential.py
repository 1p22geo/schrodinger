import numpy as np


class CoulombPotential():
    def __init__(self, config):
        self.x_center = config.Lx / 2
        self.y_center = config.Ly / 2
        self.r = np.sqrt((config.X - self.x_center)**2 + (config.Y - self.y_center)**2)
        self.V = -1 / self.r  # Central Coulomb potential

class MeanFieldPotential():
    def __init__(self, config, particle):
        self.x_center = config.Lx / 2
        self.y_center = config.Ly / 2
        self.rho = np.abs(particle.psi)**2  # Charge density of electron
        self.V = -1 / np.sqrt((config.X - self.x_center)**2 + (config.Y - self.y_center)**2 + 1e-6)  # Regularize the denominator
        self.V *= np.sum(self.rho) * config.dx * config.dy  # Scale by charge