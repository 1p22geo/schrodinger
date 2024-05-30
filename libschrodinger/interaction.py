import numpy as np

import lib.particle
import lib.config
import lib.electron
import lib.potential


class Interactions:
    """
    Static class with methods for interactions between particles.
    """
    def get_relative_potential(config: lib.config.Config,
                               particle1: lib.particle.Particle,
                               particle2: lib.particle.Particle) -> np.array:
        if not config.interactions_enabled:
            return np.zeros((config.Nx, config.Ny))
        if isinstance(particle1, lib.electron.Electron):
            if isinstance(particle2, lib.electron.Electron):
                return - 0.2 * lib.potential.MeanFieldPotential(config, particle1).V * particle1.principal_quantum * particle2.principal_quantum

        return np.zeros((config.Nx, config.Ny))
