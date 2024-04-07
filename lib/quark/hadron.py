import numpy as np
import uuid

import lib.particle
import lib.config
import lib.potential


class Hadron(lib.particle.Particle):
    """
    [HIGHLY EXPERIMENTAL] (see relevant doc for `lib.quark.quark.Quark`)

    Base class for heavy particles composed of a couple quarks
    """

    config: lib.config.Config
    """
    experiment configurations
    """
    psi: np.array
    """
    Composite wave function
    Sum of all wave functions of the quarks

    a `np.array` of shape `(config.Nx, config.Ny)`
    """
    quarks: list[lib.quark.quark.Quark]
    """
    Literally the list of involved quarks
    """

    def __init__(self, config, quarks: list[lib.quark.quark.Quark]):
        self._id = uuid.uuid4()
        self.config = config
        self.psi = np.zeros((config.Nx, config.Ny), dtype="complex128")
        self.quarks = quarks
        for q in self.quarks:
            self.psi += q.psi

    def propagate(self, V: np.array, particles: list[lib.particle.Particle]):
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

        self.psi = np.zeros(
            (self.config.Nx, self.config.Ny), dtype="complex128")
        for q in self.quarks:
            q.propagate(V, particles)
            self.psi += q.psi

        if not (self.config.interactions_enabled):
            return
        # Interact with other particles
        for p in particles:
            if p._id == self._id:
                continue
            pass
            # interact with particle
