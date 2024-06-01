import os
import shutil

import libschrodinger

config = libschrodinger.config.Config(
    a0=1, Lx=20, Ly=20, Nx=2000, Ny=2000, Nt=2000, T_max=50)

potential = libschrodinger.potential.CoulombPotential(config)


particles = [libschrodinger.electron.Electron(config, potential, 2, 1, 0)]


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
        particles.append(libschrodinger.gauss.WavePacket(
            config, x0=10, y0=10, vy=1))

    if t == 1100:
        particles[0].principal_quantum = 2
        particles[0].azimuthal_quantum = 1
        particles[0].psi = particles[0].calculate_psi(potential)
        del particles[1]

    graph = libschrodinger.graphs.GraphDisplay(config, (12, 8), frameno=t)
    for n in range(len(particles)):
        particle = particles[n]
        particle.propagate(potential.V, particles, t)
        particle.draw(graph, potential.V, 3, 2, n)

    filename = f"{dirname}/frame_{t}.png"
    graph.save(filename)

mp4 = libschrodinger.graphs.GraphDisplay(config).render_mp4(dirname)
print(f"Saved mp4 to {mp4}")
