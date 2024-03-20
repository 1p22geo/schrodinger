import matplotlib.pyplot as plt
import matplotlib
import os

import numpy as np

import lib.config
import lib.figlocation

matplotlib.use("Agg")


class GraphDisplay:
    """
    Class for displaying experiment output as a matplotlib graph into a file.
    """

    config: lib.config.Config
    """
    configuration for the domain
    """
    fig: plt.figure
    """
    the actual matplotlib `matplotlib.pypylot.figure`
    """

    def __init__(self, config, figsize=(12, 8)):
        self.config = config
        self.fig = plt.figure(figsize=figsize)

    def save(self, filename: str):
        """
        save the graph output into a file
        """
        self.fig.savefig(filename)
        print(f"Saved to {filename}")
        plt.close(self.fig)
        del self.fig

    def add_figure(
        self,
        location: lib.figlocation.FigureLocation,
        function: np.array,
        title: str = "",
        fig_type: str = "3d",
        cmap="viridis",
        zlim=(None, None),
    ):
        """
        add another subplot figure

        Currently supported figure types:
        - 'color': matplotlib contourf plot with a color bar
        - '3d': 3d plot displaying the function as a surface
        - 'simple': simple 2d color plot

        Parameters:
        - `location:lib.figlocation.FigureLocation`: the location for the subplot
        - `function:np.array`: the actual function to plot
        - `title:str`: the title of the subplot
        - `fig_title:str`: the figure type
        - `cmap` and `zlim`: kwargs for matplotlib
        """
        match fig_type:
            case "color":
                ax = self.fig.add_subplot(location.spec())
                cs = ax.contourf(self.config.X, self.config.Y, function, cmap=cmap)
                ax.set_title(title)
                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)
                self.fig.colorbar(cs)
            case "3d":
                ax = self.fig.add_subplot(location.spec(), projection="3d")
                ax.plot_surface(self.config.X, self.config.Y, function, cmap=cmap)
                ax.set_title(title)
                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)
                ax.set_zlim(zlim[0], zlim[1])
            case "simple":
                ax = self.fig.add_subplot(location.spec())
                ax.pcolormesh(self.config.X, self.config.Y, function, cmap=cmap)
                ax.set_title(title)

                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)

    def render_mp4(self, dirname):
        """
        renders images in `{dirname}/frame%d.png` into `{dirname}/movie.mp4` and `{dirname}/movie.mpg`
        """
        os.system(
            f"ffmpeg -i {dirname}/frame_%d.png -c:v mpeg2video -q:v 5 -c:a mp2 -f vob {dirname}/movie.mpg"
        )
        os.system(
            f"ffmpeg -i {dirname}/movie.mpg -c:v libx264 -c:a libfaac -crf 1 -preset:v veryslow {dirname}/movie.mp4"
        )
        mp4 = f"{dirname}/movie.mp4"
        return mp4
