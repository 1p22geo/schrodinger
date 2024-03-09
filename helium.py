import os
import numpy as np
import lib

config = lib.QuantumConfig(1, 16, 16, 2000, 2000, 4000, 300)

potential = lib.CoulombPotential(config)


el1 = lib.Electron(config, potential, 2, 1, 0)

el2 = lib.Electron(config, potential, 2, 1, 0)
el2.psi *= -1


if not os.path.exists("output_images4"):
    os.makedirs("output_images4")

frames = []

for t in range(config.Nt):
    print(f"Time: {t}")
    p1 = lib.MeanFieldPotential(config, el2)
    p2 = lib.MeanFieldPotential(config, el1)

    el1.propagate(potential.V + p1.V)
    el2.propagate(potential.V + p2.V)

    graph = lib.GraphDisplay(config)

    graph.add_figure(231, np.angle(el1.psi), "Phase (Electron 1)", "color")
    graph.add_figure(232, np.angle(el2.psi), "Phase (Electron 2)", "color")
    graph.add_figure(234, np.absolute(el1.psi), "Absolute (Electron 1)", "3d")
    graph.add_figure(235, np.absolute(el2.psi), "Absolute (Electron 2)", "3d")

    graph.add_figure(233, p1.V, "Mean potential (electron 1)", "3d")
    graph.add_figure(236, p1.V, "Potential function (central Coulomb)", "3d")

    filename = f"output_images4/frame_{t:03d}.png"
    graph.save(filename)

print("Done! Saved all images.")
