import numpy as np

class Particle():
    """
    Base class for all particles

    Attributes:
        Config config: configuration for the domain
    """
    def __init__(self, config):
        self.config = config
        self.psi = np.zeros((config.Nx, config.Ny))

    def propagate(self, particles, V):
        """
        propagate the wave function in a potential field

        Attributes:
            np.array V: the potential field as an array
                of shape (Nx, Ny)
            Particle[] particles: an array of other particles 
                for inter-particle interactions
        """
        pass