import os
import numpy as np
import lib.constants as constants

config = constants.Config(1, 20, 20, 2000, 2000, 2000, 50)

potential = constants.CoulombPotential(config)


particles = [constants.Electron(config, potential, 2, 1, 0)]


dirname = "output_images"
if not os.path.exists(dirname):
    os.makedirs(dirname)

frames = []
for t in range(config.Nt):
    if t == 400:
        particles[0].principal_quantum = 1
        particles[0].azimuthal_quantum = 0
        particles[0].psi = particles[0].calculate_psi(potential)
        particles.append(constants.Photon(config, x0=10, y0=10, vx=1))

    graph = constants.GraphDisplay(config, (12, 4 * len(particles)))
    for n in range(len(particles)):
        particle = particles[n]
        particle.propagate(potential.V, particles)

        graph.add_figure(
            constants.FigureLocation(len(particles), 3, 3 * n),
            np.angle(particle.psi),
            f"Phase (particle {n})",
            "color",
        )
        graph.add_figure(
            constants.FigureLocation(len(particles), 3, 3 * n + 1),
            np.absolute(particle.psi),
            f"Absolute (particle {n})",
            "3d",
        )
        graph.add_figure(
            constants.FigureLocation(len(particles), 3, 3 * n + 2),
            potential.V,
            f"Mean potential field (particle {n})",
            "3d",
            cmap=None,
            zlim=(-1, 0),
        )
    filename = f"{dirname}/frame_{t}.png"
    graph.save(filename)


print("Done! Saved all images.")
