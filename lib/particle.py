import numpy as np

import lib.config


class Particle:
    """
    Base class for all particles
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
    _fig_opts: dict
    """
    Additional kwargs to `lib.graphs.GraphDisplay.add_figure`

    or to `matplotlib.pyplot`
    """

    def __init__(self, config):
        self.config = config
        self.psi = np.zeros((config.Nx, config.Ny))
        self._fig_opts = {}

    def propagate(self, V: np.array, particles: list["lib.particle.Particle"]):
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
        pass
