import numpy as np
import uuid

import lib.particle
import lib.config
import lib.potential
import lib.quark.quark


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
    colors: np.array
    """
    Colors which can be passed as **facecolors to matplotlib or
    `lib.graphs.GraphDisplay.add_figure`
    """

    def __init__(self, config, quarks: list[lib.quark.quark.Quark]):
        self._id = uuid.uuid4()
        self.config = config
        self.psi = np.zeros((config.Nx, config.Ny), dtype="complex128")
        self.quarks = quarks
        self.colors = np.zeros((config.Nx, config.Ny, 3))
        for q in self.quarks:
            self.psi += q.psi

    def draw(self, graph: "lib.graphs.GraphDisplay", V: np.array, x, y, num):
        """
        Draws self as graphs (`3*num`, `3*num+1`, `3*num+2`)
        on an `x` by `y` figure in `graph`

        Or if this is particle number `num`
        and graphs are made on a `x` by `y` grid
        """
        graph.add_figure(
            lib.figlocation.FigureLocation(x, y, 3 * num),
            np.angle(self.psi),
            f"Phase (particle {num})",
            "color",
        )
        graph.add_figure(
            lib.figlocation.FigureLocation(x, y, 3 * num + 1),
            np.absolute(self.psi),
            f"Absolute (particle {num})",
            "3d",
            facecolors=self.colors,
        )

        graph.add_figure(
            lib.figlocation.FigureLocation(x, y, 3 * num + 2),
            V,
            f"Mean potential (particle {num})",
            "3d",
            zlim=(-1, 0),
            cmap=None,
        )

    def propagate(
        self, V: np.array, particles: list[lib.particle.Particle], frame: int
    ):
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
            q.propagate(V, particles, frame)
            self.psi += q.psi

        if not (self.config.interactions_enabled):
            return
        # Interact with other particles
        for p in particles:
            if p._id == self._id:
                continue
            pass
            # interact with particle
