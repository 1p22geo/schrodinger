import numpy as np
import flask
import uuid
import time
import os

from engine.deserialization import Deserializer

import lib.graphs
import lib.figlocation
import lib.constants


def renderpreview(state):
    print(state)
    start = time.time_ns()
    config, potentials, particles = Deserializer().ds(state)

    graph = lib.graphs.GraphDisplay(config, (12, 4 * len(particles)))

    for n in range(len(particles)):
        particle = particles[n]
        V_total = np.zeros((config.Nx, config.Ny))
        for potential in potentials:
            V_total += potential.V
        for p2 in particles:
            if p2._id != particle._id:
                V_total +=\
                    lib.interaction.\
                    Interactions.get_relative_potential(
                        config, particle, p2)

        particle.draw(graph, V_total, len(particles), 3, n)
    filename = uuid.uuid4()
    filename = f"static/temp/{filename}.png"
    if not os.path.exists("static/temp"):
        os.makedirs("static/temp")
    graph.save(filename)

    end = time.time_ns()
    frame_time = end - start
    eta = frame_time * config.Nt
    if config.interactions_enabled:
        eta *= 2  # that meson emmision is really unoptimised

    days = int(eta / lib.constants.NS_IN_DAY)
    hours = round((eta % lib.constants.NS_IN_DAY) /
                  lib.constants.NS_IN_HOUR, 2)

    res = flask.send_file(filename)
    res.headers["X-ETA-To-Full-Animation"] = f"{days} days, {hours} hours"
    return res
