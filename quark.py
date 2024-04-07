import os
import math
import numpy as np

import lib.config
import lib.potential
import lib.electron
import lib.graphs
import lib.figlocation

import lib.quark.quark
import lib.quark.baryon

config = lib.config.Config(0.7, 10, 10, 2000, 2000, 10, 1)

potential = lib.potential.CoulombPotential(config)


if not os.path.exists("output_images4"):
    os.makedirs("output_images4")

frames = []

for t in range(config.Nt):
    print(f"Time: {t}")

    graph = lib.graphs.GraphDisplay(config, figsize=(12, 4))
    particle = lib.quark.baryon.Baryon(config)

    particle.draw(graph, potential, 1, 3, 0)

    filename = f"output_images4/frame_{t:03d}.png"
    graph.save(filename)

print("Done! Saved all images.")
