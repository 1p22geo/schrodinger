import numpy as np
import flask
import lib
import uuid
import time
import os
from engine.deserialization import Deserializer


def renderpreview(state):
    print(state)
    start = time.time_ns()
    config, potential, particles = Deserializer().ds(state)

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
            potential.V,
            f"Mean potential field (particle {n})",
            "3d",
            zlim=(-1, 0),
            cmap=None,
        )
    filename = uuid.uuid4()
    filename = f"static/temp/{filename}.png"
    if not os.path.exists("static/temp"):
        os.makedirs("static/temp")
    graph.save(filename)

    end = time.time_ns()
    frame_time = end - start
    eta = frame_time * config.Nt

    days = int(eta / lib.NS_IN_DAY)
    hours = round((eta % lib.NS_IN_DAY) / lib.NS_IN_HOUR, 2)

    res = flask.send_file(filename)
    res.headers["X-ETA-To-Full-Animation"] = f"{days} days, {hours} hours"
    return res
