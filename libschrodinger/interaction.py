import numpy as np

import libschrodinger.particle
import libschrodinger.config
import libschrodinger.electron
import libschrodinger.potential


class Interactions:
    """
    Static class with methods for interactions between particles.
    """
    def get_relative_potential(config: libschrodinger.config.Config,
                               particle1: libschrodinger.particle.Particle,
                               particle2: libschrodinger.particle.Particle) -> np.array:
        if not config.interactions_enabled:
            return np.zeros((config.Nx, config.Ny))
        if isinstance(particle1, libschrodinger.electron.Electron):
            if isinstance(particle2, libschrodinger.electron.Electron):
                return - 0.2 * libschrodinger.potential.MeanFieldPotential(config, particle1).V * particle1.principal_quantum * particle2.principal_quantum

        return np.zeros((config.Nx, config.Ny))
