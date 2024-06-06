import numpy as np
import uuid

import libschrodinger.particle
import libschrodinger.config
import libschrodinger.potential
import libschrodinger.quark.quark
import libschrodinger.figlocation


class Hadron(libschrodinger.particle.Particle):
    """
    [HIGHLY EXPERIMENTAL] (see relevant doc for `libschrodinger.quark.quark.Quark`)

    Base class for heavy particles composed of a couple quarks
    """

    config: libschrodinger.config.Config
    """
    experiment configurations
    """
    psi: np.ndarray
    """
    Composite wave function
    Sum of all wave functions of the quarks

    a `np.array` of shape `(config.Nx, config.Ny)`
    """
    quarks: list[libschrodinger.quark.quark.Quark]
    """
    Literally the list of involved quarks
    """
    colors: np.ndarray
    """
    Colors which can be passed as **facecolors to matplotlib or
    `libschrodinger.graphs.GraphDisplay.add_figure`
    """

    def __init__(self, config, quarks: list[libschrodinger.quark.quark.Quark]):
        self.__id = uuid.uuid4()
        self.config = config
        self.psi = np.zeros((config.Nx, config.Ny), dtype="complex128")
        self.quarks = quarks
        self.colors = np.zeros((config.Nx, config.Ny, 3))
        for q in self.quarks:
            self.psi += q.psi

    def draw(self, graph: "libschrodinger.graphs.GraphDisplay", V: np.ndarray, x, y, num):
        """
        Draws self as graphs (`3*num`, `3*num+1`, `3*num+2`)
        on an `x` by `y` figure in `graph`

        Or if this is particle number `num`
        and graphs are made on a `x` by `y` grid
        """
        graph.add_figure(
            libschrodinger.figlocation.FigureLocation(x, y, 3 * num),
            np.angle(self.psi),
            f"Phase (particle {num})",
            "color",
        )
        graph.add_figure(
            libschrodinger.figlocation.FigureLocation(x, y, 3 * num + 1),
            np.absolute(self.psi),
            f"Absolute (particle {num})",
            "3d",
            facecolors=self.colors,
        )

        graph.add_figure(
            libschrodinger.figlocation.FigureLocation(x, y, 3 * num + 2),
            V,
            f"Mean potential (particle {num})",
            "3d",
            zlim=(-1, 0),
            cmap=None,
        )

    def propagate(
        self, V: np.ndarray, particles: list[libschrodinger.particle.Particle], frame: int
    ) -> list["libschrodinger.particle.Particle"] | None:
        """
        propagate the wave function in a potential field

        Parameters
        ----------
        - `V: np.ndarray`
            - the potential field as an array
            of shape (Nx, Ny)
        - `particles: list[libschrodinger.particle.Particle]`
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
            if p._id == self.__id:
                continue
            pass
            # interact with particle
