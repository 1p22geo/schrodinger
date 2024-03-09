import numpy as np
import flask
import lib
import uuid
import time


def renderpreview(state):
    start = time.time_ns()
    dc = state["config"]["domain"]
    config = lib.QuantumConfig(
        1, dc["x"], dc["y"], dc["Nx"], dc["Ny"], dc["Nt"], dc["T_max"]
    )

    serialized_particles = state["particles"]
    particles = []
    for sp in serialized_particles:
        match sp["type"]:
            case "electron":
                particles.append(
                    lib.Electron(
                        config,
                        lib.CoulombPotential(config),
                        sp["principal_quantum"],
                        sp["azimuthal_quantum"],
                        sp["magnetic_quantum"],
                    )
                )

    graph = lib.GraphDisplay(config, (12, 4 * len(particles)))

    for n in range(len(particles)):
        particle = particles[n]
        graph.add_figure(
            lib.FigureLocation(len(particles), 3, 3 * n),
            np.angle(particle.psi),
            f"Phase (particle {n})",
            "color",
        )
        graph.add_figure(
            lib.FigureLocation(len(particles), 3, 3 * n + 1),
            np.absolute(particle.psi),
            f"Absolute (particle {n})",
            "3d",
        )
        graph.add_figure(
            lib.FigureLocation(len(particles), 3, 3 * n + 2),
            lib.CoulombPotential(config).V,
            f"Mean potential field (particle {n})",
            "3d",
        )
    filename = uuid.uuid4()
    filename = f"static/temp/{filename}.png"
    graph.save(filename)

    end = time.time_ns()
    frame_time = end - start
    eta = frame_time * config.Nt

    days = int(eta / lib.NS_IN_DAY)
    hours = round((eta % lib.NS_IN_DAY) / lib.NS_IN_HOUR, 2)

    res = flask.send_file(filename)
    res.headers["X-ETA-To-Full-Animation"] = f"{days} days, {hours} hours"
    return res
