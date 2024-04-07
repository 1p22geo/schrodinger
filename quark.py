import os
import math
import numpy as np

import lib.config
import lib.potential
import lib.electron
import lib.graphs
import lib.figlocation

import lib.quark.quark
import lib.quark.hadron

config = lib.config.Config(0.7, 10, 10, 2000, 2000, 10, 1)

potential = lib.potential.CoulombPotential(config)


if not os.path.exists("output_images4"):
    os.makedirs("output_images4")

frames = []

for t in range(config.Nt):
    print(f"Time: {t}")

    graph = lib.graphs.GraphDisplay(config, figsize=(12, 4))
    colors = np.zeros((config.Nx, config.Ny, 3))
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
            colors[x][y] = np.array((r, g, b))

    particle = lib.quark.hadron.Hadron(config, [
        lib.quark.quark.Quark(config, 2.0, 5.0),
        lib.quark.quark.Quark(config, 6.5, 5.0-1.5*math.sqrt(3)),
        lib.quark.quark.Quark(config, 6.5, 5.0+1.5*math.sqrt(3))
    ])

    graph.add_figure(
        lib.figlocation.FigureLocation(1, 3, 0),
        np.angle(particle.psi),
        "Phase (Electron 1)",
        "color",
    )
    graph.add_figure(
        lib.figlocation.FigureLocation(1, 3, 1),
        np.absolute(particle.psi),
        "Absolute (Electron 1)",
        "3d",
        facecolors=colors,
    )

    graph.add_figure(
        lib.figlocation.FigureLocation(1, 3, 2),
        potential.V,
        "Mean potential (electron 1)",
        "3d",
        zlim=(-1, 0),
        cmap=None,
    )

    filename = f"output_images4/frame_{t:03d}.png"
    graph.save(filename)

print("Done! Saved all images.")
