import os
import numpy as np
import libschrodinger

config = libschrodinger.config.Config(1, 20, 20, 4000, 4000, 2000, 100)

proton_1 = libschrodinger.potential.CoulombPotential(
    config, x_center=10, y_center=5)
proton_2 = libschrodinger.potential.CoulombPotential(
    config, x_center=10, y_center=15)


el1 = libschrodinger.electron.Electron(config, proton_1, 1, 0, 0)

el2 = libschrodinger.electron.Electron(config, proton_2, 1, 0, 0)
el2.psi *= -1


if not os.path.exists("output_images"):
    os.makedirs("output_images")

frames = []
particles = [el1, el2]

for t in range(config.Nt):
    print(f"Time: {t}")
    merged = 1
    if t <= 1000:
        merged = t / 1000
        el1.psi = np.roll(el1.psi, 1, axis=0)
        el2.psi = np.roll(el2.psi, -1, axis=0)

    proton_1 = libschrodinger.potential.CoulombPotential(
        config, x_center=10, y_center=(5 + merged * 5)
    )
    proton_2 = libschrodinger.potential.CoulombPotential(
        config, x_center=10, y_center=(15 - merged * 5)
    )

    potential_1 = proton_1.V + proton_2.V
    potential_2 = proton_1.V + proton_2.V

    el1.propagate(potential_1, particles, t)
    el2.propagate(potential_2, particles, t)

    graph = libschrodinger.graphs.GraphDisplay(config)

    el1.draw(graph, potential_1, 3, 2, 0)
    el2.draw(graph, potential_2, 3, 2, 1)

    filename = f"output_images/frame_{t}.png"
    graph.save(filename)

mp4 = graph.render_mp4("output_images")
print(f"Done! MP4 saved to {mp4}")
