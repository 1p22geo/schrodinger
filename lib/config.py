import numpy as np


class Config:
    """
    Configuration for an experiment.
    """

    a0: float
    """
    the Bohr radius. Better to leave it as default.
    """
    Lx: float
    """
    size of the domain in x
    """
    Ly: float
    """
    size of the domain in y
    """
    Nx: int
    """
    resolution of the domain in x
    """
    Ny: int
    """
    resolution of the domain in y
    """
    Nt: int
    """
    amount of time-steps
    """
    T_max: float
    """
    length of experiment
    """
    dt: float
    """
    length of a single time-step
    """
    dx: float
    """
    length of a single division on X axis
    """
    dy: float
    """
    length of a single division on Y axis
    """
    x: np.array
    """
    a linear space from 0 to Lx with a resolution of Nx  
    can be used in calculating psi
    """
    y: np.array
    """
    a linear space from 0 to Ly with a resolution of Ny  
    can be used in calculating psi
    """
    interactions_enabled: bool
    """
    enables experimental particle interactions

    please leave it at False.
    """

    def __init__(self, a0=1.0, Lx=10, Ly=10, Nx=1000, Ny=1000, Nt=2000, T_max=10):
        self.a0 = a0
        self.Lx = Lx
        self.Ly = Ly
        self.Nx = Nx
        self.Ny = Ny
        self.Nt = Nt
        self.T_max = T_max
        self.dt = T_max / Nt  # Time step
        self.x = np.linspace(0, Lx, Nx)
        self.y = np.linspace(0, Ly, Ny)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
        self.interactions_enabled = False
