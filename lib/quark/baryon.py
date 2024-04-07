import numpy as np
import math

import lib.quark.hadron


class Baryon(lib.quark.hadron.Hadron):
    """
    Equally abstract [and EXPERIMENTAL] class for baryons.

    But hey, colors! :3
    """

    colors: np.array
    """
    Colors which can be passed as **facecolors to matplotlib or
    `lib.graphs.GraphDisplay.add_figure`
    """

    def __init__(self, config):
        super().__init__(config, [
            lib.quark.quark.Quark(config, 2.0, 5.0),
            lib.quark.quark.Quark(config, 6.5, 5.0-1.5*math.sqrt(3)),
            lib.quark.quark.Quark(config, 6.5, 5.0+1.5*math.sqrt(3))
        ])
        self.colors = np.zeros((config.Nx, config.Ny, 3))
        """
        I am sorry. This is terrible quality code.
        I should check for the ACTUAL angular distance.

        For instance, the distance between 2*pi and 0.5*pi
        is not 1.5*pi but 0.5*pi

        But I am lazy.
        And red is both 0 and 2*pi
        """

        R = 0 * math.pi / 3
        R2 = 6 * math.pi / 3
        G = 2 * math.pi / 3
        B = 4 * math.pi / 3
        for x in range(config.Nx):
            for y in range(config.Ny):
                x_norm = x - config.Nx / 2
                y_norm = y - config.Ny / 2
                theta = np.angle(x_norm + 1j * y_norm)
                theta += math.pi
                r = max(1 - abs(R - theta) ** 4, 1 - abs(R2 - theta) ** 4, 0)
                g = max(1 - abs(G - theta) ** 4, 0)
                b = max(1 - abs(B - theta) ** 4, 0)
                self.colors[x][y] = np.array((r, g, b))

    def draw(self,
             graph: "lib.graphs.GraphDisplay",
             potential: "lib.potential.Potential",
             x,
             y,
             num):
        """
        Draws self as graphs (`3*num`, `3*num+1`, `3*num+2`)
        on an `x` by `y` figure in `graph`

        Or if this is particle number `num`
        and graphs are made on a `x` by `y` grid
        """
        graph.add_figure(
            lib.figlocation.FigureLocation(x, y, num),
            np.angle(self.psi),
            "Phase (Electron 1)",
            "color",
        )
        graph.add_figure(
            lib.figlocation.FigureLocation(1, 3, 1),
            np.absolute(self.psi),
            "Absolute (Electron 1)",
            "3d",
            facecolors=self.colors,
        )

        graph.add_figure(
            lib.figlocation.FigureLocation(1, 3, 2),
            potential.V,
            "Mean potential (electron 1)",
            "3d",
            zlim=(-1, 0),
            cmap=None,
        )
