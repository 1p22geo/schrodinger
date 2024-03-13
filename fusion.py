import os
import numpy as np
import lib

config = lib.Config(1, 10, 20, 4000, 4000, 4000, 200)

proton_1 = lib.CoulombPotential(config, x_center=5, y_center=5)
proton_2 = lib.CoulombPotential(config, x_center=5, y_center=15)


el1 = lib.Electron(config, proton_1, 2, 1, 0)

el2 = lib.Electron(config, proton_2, 2, 1, 0)
el2.psi *= -1


if not os.path.exists("output_images"):
    os.makedirs("output_images")

frames = []

for t in range(config.Nt):
    print(f"Time: {t}")
    potential_1 = lib.MeanFieldPotential(
        config, el2).V + proton_1.V + proton_2.V
    potential_2 = lib.MeanFieldPotential(
        config, el1).V + proton_1.V + proton_2.V

    el1.propagate(potential_1)
    el2.propagate(potential_2)

    graph = lib.GraphDisplay(config)

    graph.add_figure(
        lib.FigureLocation(2, 3, 0), np.angle(
            el1.psi), "Phase (Electron 1)", "color"
    )
    graph.add_figure(
        lib.FigureLocation(2, 3, 3), np.angle(
            el2.psi), "Phase (Electron 2)", "color"
    )
    graph.add_figure(
        lib.FigureLocation(2, 3, 1), np.absolute(
            el1.psi), "Absolute (Electron 1)", "3d"
    )
    graph.add_figure(
        lib.FigureLocation(2, 3, 4), np.absolute(
            el2.psi), "Absolute (Electron 2)", "3d"
    )
    graph.add_figure(
        lib.FigureLocation(2, 3, 2), proton_1.V, "Potential (proton 1)", "3d"
    )
    graph.add_figure(
        lib.FigureLocation(2, 3, 5), proton_2.V, "Potential (proton 2)", "3d"
    )

    filename = f"output_images/frame_{t}.png"
    graph.save(filename)

mp4 = graph.render_mp4("output_images")
print(f"Done! MP4 saved to {mp4}")
