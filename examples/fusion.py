import os
import numpy as np
import lib.constants as constants

config = constants.Config(1, 20, 20, 4000, 4000, 2000, 100)

proton_1 = constants.CoulombPotential(config, x_center=10, y_center=5)
proton_2 = constants.CoulombPotential(config, x_center=10, y_center=15)


el1 = constants.Electron(config, proton_1, 1, 0, 0)

el2 = constants.Electron(config, proton_2, 1, 0, 0)
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

    proton_1 = constants.CoulombPotential(
        config, x_center=10, y_center=(5 + merged * 5)
    )
    proton_2 = constants.CoulombPotential(
        config, x_center=10, y_center=(15 - merged * 5)
    )

    potential_1 = proton_1.V + proton_2.V
    potential_2 = proton_1.V + proton_2.V

    el1.propagate(potential_1, particles)
    el2.propagate(potential_2, particles)

    graph = constants.GraphDisplay(config)

    graph.add_figure(
        constants.FigureLocation(2, 3, 0),
        np.angle(el1.psi),
        "Phase (Electron 1)",
        "color",
    )
    graph.add_figure(
        constants.FigureLocation(2, 3, 3),
        np.angle(el2.psi),
        "Phase (Electron 2)",
        "color",
    )
    graph.add_figure(
        constants.FigureLocation(2, 3, 1),
        np.absolute(el1.psi),
        "Absolute (Electron 1)",
        "3d",
    )
    graph.add_figure(
        constants.FigureLocation(2, 3, 4),
        np.absolute(el2.psi),
        "Absolute (Electron 2)",
        "3d",
    )
    graph.add_figure(
        constants.FigureLocation(2, 3, 2),
        proton_1.V,
        "Potential (proton 1)",
        "3d",
        cmap=None,
        zlim=(-1, 0),
    )
    graph.add_figure(
        constants.FigureLocation(2, 3, 5),
        proton_2.V,
        "Potential (proton 2)",
        "3d",
        cmap=None,
        zlim=(-1, 0),
    )

    filename = f"output_images/frame_{t}.png"
    graph.save(filename)

mp4 = graph.render_mp4("output_images")
print(f"Done! MP4 saved to {mp4}")