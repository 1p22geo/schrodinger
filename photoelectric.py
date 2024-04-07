import os
import numpy as np
import shutil

import lib.config
import lib.potential
import lib.electron
import lib.gauss
import lib.graphs
import lib.figlocation

config = lib.config.Config(a0=1, Lx=20, Ly=20, Nx=2000, Ny=2000, Nt=2000, T_max=50)

potential = lib.potential.CoulombPotential(config)


particles = [lib.electron.Electron(config, potential, 2, 1, 0)]


dirname = "output_images"
if os.path.exists(dirname):
    shutil.rmtree(dirname, ignore_errors=True)

if not os.path.exists(dirname):
    os.makedirs(dirname)

frames = []
for t in range(config.Nt):
    if t == 400:
        particles[0].principal_quantum = 1
        particles[0].azimuthal_quantum = 0
        particles[0].psi = particles[0].calculate_psi(potential)
        particles.append(lib.gauss.WavePacket(config, x0=10, y0=10, vy=1))

    if t == 1100:
        particles[0].principal_quantum = 2
        particles[0].azimuthal_quantum = 1
        particles[0].psi = particles[0].calculate_psi(potential)
        del particles[1]

    graph = lib.graphs.GraphDisplay(config, (12, 8), frameno=t)
    for n in range(len(particles)):
        particle = particles[n]
        particle.propagate(potential.V, particles)

        graph.add_figure(
            lib.figlocation.FigureLocation(2, 3, 3 * n),
            np.angle(particle.psi),
            f"Phase (particle {n})",
            "color",
        )
        graph.add_figure(
            lib.figlocation.FigureLocation(2, 3, 3 * n + 1),
            np.absolute(particle.psi),
            f"Absolute (particle {n})",
            "3d",
        )
        graph.add_figure(
            lib.figlocation.FigureLocation(2, 3, 3 * n + 2),
            potential.V,
            f"Mean potential field (particle {n})",
            "3d",
            cmap=None,
            zlim=(-1, 0),
        )
    filename = f"{dirname}/frame_{t}.png"
    graph.save(filename)

mp4 = lib.graphs.GraphDisplay(config).render_mp4(dirname)
print(f"Saved mp4 to {mp4}")
