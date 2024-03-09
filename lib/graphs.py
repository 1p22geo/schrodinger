import matplotlib.pyplot as plt


class GraphDisplay:
    """
    Class for displaying experiment output as a matplotlib graph into a file.

    Attributes:
        Config config: experiment config
        tuple<int> figsize: size of the graph display
    """

    def __init__(self, config, figsize=(12, 8)):
        self.config = config
        self.fig = plt.figure(figsize=figsize)

    def save(self, filename):
        """
        save the graph output into a file
        """
        plt.savefig(filename)
        print(f"Saved to {filename}")
        plt.close()

    def add_figure(self, location, function, title="", fig_type="3d"):
        """
        add another subplot figure

        Currently supported figure types:
        - 'color': matplotlib contourf plot with a color bar
        - '3d': 3d plot displaying the function as a surface
        - 'simple': simple 2d color plot

        Parameters:
            int location: the matplotlib location for the subplot
                location 235 means the fifth graph on a 2x3 grid
                location 132 means the second graph on a 1x3 grid
            np.array function: the values of the function, as an array or List.
                suggested array shape: (Nx, Ny)
            str title: title of the sublot (displayed above it)
            str fig_type: the type of the figure
        """
        match fig_type:
            case "color":
                ax = self.fig.add_subplot(location)
                cs = ax.contourf(self.config.X, self.config.Y, function)
                ax.set_title(title)
                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)
                self.fig.colorbar(cs)
            case "3d":
                ax = self.fig.add_subplot(location, projection="3d")
                ax.plot_surface(self.config.X, self.config.Y, function, cmap="viridis")
                ax.set_title(title)
                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)
            case "simple":
                ax = self.fig.add_subplot(location)
                ax.pcolormesh(self.config.X, self.config.Y, function)
                ax.set_title(title)

                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)
