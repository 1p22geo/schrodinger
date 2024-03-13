import numpy as np


class Config:
    """
    Configuration for an experiment.

    Atributes:
        float a0: the Bohr radius. Better to leave it as default.
        float Lx: size of the domain in x
        float Ly: size of the domain in y
        int Nx: resolution of the domain in x
        int Ny: resolution of the domain in y
        int Nt: amount of time-steps
        float T_max: duration of the experiment
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
