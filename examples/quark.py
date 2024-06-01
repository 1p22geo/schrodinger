import os

import libschrodinger

config = libschrodinger.config.Config(0.7, 10, 10, 2000, 2000, 10, 1)

potential = libschrodinger.potential.CoulombPotential(config)

particles = [libschrodinger.quark.meson.Meson(
    config, 5, 5, 1, 3, 2, libschrodinger.quark.color.COLOR.RED, libschrodinger.quark.color.COLOR.ANTIRED)]

if not os.path.exists("output_images4"):
    os.makedirs("output_images4")

frames = []

for t in range(config.Nt):
    print(f"Time: {t}")

    graph = libschrodinger.graphs.GraphDisplay(config, figsize=(12, 8))

    for n in range(len(particles)):
        particle = particles[n]

        particle.draw(graph, potential.V, 2, 3, n)
        particle.propagate(potential.V, particles, n)

    filename = f"output_images4/frame_{t:03d}.png"
    graph.save(filename)

print("Done! Saved all images.")
