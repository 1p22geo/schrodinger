import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class GraphDisplay():
    def __init__(self, config):
        self.config = config
        self.fig = plt.figure(figsize=(12, 8))

    def save(self, filename):
        plt.savefig(filename)
        print(f"Saved to {filename}")
        plt.close()

    
    def add_figure(self, location, function, title="", fig_type='3d'):
        match fig_type:
            case 'color':
                ax = self.fig.add_subplot(location)
                cs = ax.contourf(self.config.X, self.config.Y, function)
                ax.set_title(title)
                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)
                cbar = self.fig.colorbar(cs)
            case '3d':
                ax = self.fig.add_subplot(location, projection='3d')
                ax.plot_surface(self.config.X, self.config.Y, function, cmap='viridis')
                ax.set_title(title)
                ax.set_xlim(0, self.config.Lx)
                ax.set_ylim(0, self.config.Ly)

