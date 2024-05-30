import numpy as np

import libschrodinger.config


class Potential:
    """
    The base class for a potential field
    """

    config: libschrodinger.config.Config
    """
    configuration for the domain
    """
    x_center: float | None
    """
    defaults to center of domain,
          the centerpoint of the potential
    """
    y_center: float | None
    """
    defaults to center of domain,
          the centerpoint of the potential
    """
    r: np.array
    """
    A `np.array` of shape `(Nx, Ny)` where each point
    is assigned its distance from `(x_center, y_center)`.

    Only for internal use in calculating V.
    """
    V: np.array
    """
    An initially zero-filled `np.array` of shape `(Nx, Ny)`
    """

    def __init__(self, config, x_center=None, y_center=None):
        self.x_center = x_center if x_center else config.Lx / 2
        self.y_center = y_center if y_center else config.Ly / 2
        self.r = np.sqrt(
            (config.X - self.x_center) ** 2 + (config.Y - self.y_center) ** 2
        )
        self.V = np.zeros((config.Nx, config.Ny))
        self.V[:, :] = 0


class CoulombPotential(Potential):
    """
    Class representing a central Coulomb potential.
    Simply represents a proton or other positive charge in the
        potential centerpoint

    Atrributes same as Potential.

    """

    V: np.array
    """
    The actual potential field definition.

    A `np.array` of shape `(Nx, Ny)`
    """
    charge: float
    """
    A linear multiplier to the force.

    Which is kinda what electric charge does to electrostatic force.
    """

    def __init__(self, config, *args, charge=1, **kwargs):
        """
        Theoretically the electron is negative and this one is positive.
        But this is quantum physics.

        Also some fancy people have a negative sign in front of "attracting"
        forces, and positive for repelling forces. Whatever

        Also, `charge` is actually q1*q2
        """
        self.charge = charge
        super().__init__(config, *args, **kwargs)
        self.V = -charge / self.r


class MeanFieldPotential(Potential):
    """
    Class representing a mean field potential.
    Simply represents an electron with a wave function pushing away
        other electons with a like-signed charge.

    Atrributes same as Potential.

    """

    V: np.array
    """
    The actual potential field definition.

    A `np.array` of shape `(Nx, Ny)`
    """

    rho: np.array
    """
    The `rho` parameter of the potential

    A `np.array` of shape `(Nx, Ny)`
    """

    def __init__(self, config, particle, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.rho = np.abs(particle.psi) ** 2  # Charge density of electron
        self.V = -1 / np.sqrt(
            (config.X - self.x_center) ** 2 +
            (config.Y - self.y_center) ** 2 + 1e-6
        )  # Regularize the denominator
        self.V *= np.sum(self.rho) * config.dx * config.dy  # Scale by charge
