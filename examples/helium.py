import os
import numpy as np
import libschrodinger

config = libschrodinger.config.Config(1, 16, 16, 2000, 2000, 4000, 300)

potential = libschrodinger.potential.CoulombPotential(config)


el1 = libschrodinger.electron.Electron(config, potential, 2, 1, 0)

el2 = libschrodinger.electron.Electron(config, potential, 2, 1, 0)
el2.psi *= -1


if not os.path.exists("output_images4"):
    os.makedirs("output_images4")

frames = []

for t in range(config.Nt):
    print(f"Time: {t}")
    p1 = libschrodinger.potential.MeanFieldPotential(config, el2)
    p2 = libschrodinger.potential.MeanFieldPotential(config, el1)

    el1.propagate(potential.V + p1.V, [el1, el2], t)
    el2.propagate(potential.V + p2.V, [el1, el2], t)

    graph = libschrodinger.graphs.GraphDisplay(config)

    el1.draw(graph, potential.V + p1.V, 3, 2, 0)
    el2.draw(graph, potential.V + p2.V, 3, 2, 1)
    filename = f"output_images4/frame_{t:03d}.png"
    graph.save(filename)

print("Done! Saved all images.")
