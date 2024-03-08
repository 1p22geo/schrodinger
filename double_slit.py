import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import lib

config = lib.QuantumConfig(1, 10, 10, 1000, 1000, 3000, 200)

# Define the potential function (you can modify this)
potential = lib.EmptyPotential(config)
potential.V[:, int(3.5* config.Ny // 8): int(4 * config.Ny // 8)] = 1000000
potential.V[int(2.7*config.Nx / 7): int(3.2*config.Nx / 7), :] = 0
potential.V[int(3.8*config.Nx / 7): int(4.3*config.Nx / 7), :] = 0

# Initial wave function (Gaussial wave packet)
particle = lib.WavePacket(config, 0.5, 2.0, 2.0, 2.0, 5.0)


# Create a directory to store the PNG images
import os
if not os.path.exists("output_images"):
    os.makedirs("output_images")

# Time evolution loop
for t in range(config.Nt):
    print(f"Time: {t}")
    particle.propagate(potential.V)

    graph = lib.GraphDisplay(config, (20, 8))


    graph.add_figure(131, np.absolute(particle.psi), "Absolute", 'simple')
    graph.add_figure(132, np.angle(particle.psi), "Phase", 'simple')
    graph.add_figure(133, potential.V, "Potential function", 'simple')

    filename = f'output_images/frame_{t:03d}.png'
    graph.save(filename)


print("Done! Saved all images.")
