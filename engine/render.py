import numpy as np
import flask
import uuid
import json
import threading
import os
from engine.deserialization import Deserializer

import libschrodinger.graphs
import libschrodinger.figlocation
import libschrodinger.interaction

renders = []


class QueuedRender:
    def __init__(self, state):
        self.state = "RENDERING"
        self.latest = None
        self.frame = 0
        self.mp4 = None
        self.maxframe = state["config"]["domain"]["Nt"]
        self.thread = threading.Thread(target=self.render, args=(state,))
        self.thread.start()

    def render(self, state):
        config, potentials, particles = Deserializer().ds(state)

        dirname = uuid.uuid4()
        dirname = f"static/temp/{dirname}"

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        for t in range(config.Nt):
            graph = libschrodinger.graphs.GraphDisplay(
                config, (12, 4 * len(particles)), t)
            for n in range(len(particles)):
                particle = particles[n]
                V_total = np.zeros((config.Nx, config.Ny))
                for potential in potentials:
                    V_total += potential.V
                for p2 in particles:
                    if p2._id != particle._id:
                        V_total +=\
                            libschrodinger.interaction.\
                            Interactions.get_relative_potential(
                                config, particle, p2)

                particle.draw(graph, V_total, len(particles), 3, n)

                # bodge for deleting particles mid-loop
                new_particles = particle.propagate(V_total, particles[:], t)
                if new_particles:
                    old_particles = particles[:]
                    particles = new_particles
                    if len(old_particles) != len(new_particles):
                        break

            filename = f"{dirname}/frame_{t}.png"
            graph.save(filename)
            self.latest = filename
            self.frame = t

        print("Files ready. Rendering to MP4.")
        self.state = "RENDERING_MP4"
        os.system(
            " ".join(
                [
                    f"ffmpeg -i {dirname}/frame_%d.png",
                    "-c:v mpeg2video -q:v 5 -c:a mp2",
                    f"-f vob {dirname}/movie.mpg",
                ]
            )
        )
        os.system(
            " ".join(
                [
                    f"ffmpeg -i {dirname}/movie.mpg",
                    "-c:v libx264 -c:a libfaac -crf 1",
                    f"-preset:v veryslow {dirname}/movie.mp4",
                ]
            )
        )
        self.mp4 = f"{dirname}/movie.mp4"
        self.state = "READY"


def queue_render(state):
    renders.append(QueuedRender(state))
    render_id = len(renders) - 1
    return flask.Response(
        json.dumps(
            {"id": render_id, "preview_url": f"/api/preview?id={render_id}"}),
        status=202,
    )


def preview_render(render_id):
    try:
        renderstate = renders[render_id].state
        latest = renders[render_id].latest
        frame = renders[render_id].frame
        maxframe = renders[render_id].maxframe
        reload = ""
        if not latest or renderstate == "RENDERING_MP4":
            reload = "setTimeout(()=>{window.location.reload()}, 1000)"
        onload = ""
        if renderstate == "RENDERING":
            renderstate = f"{renderstate} frame {frame}/{maxframe}"
            onload = """
document.querySelector("img").onload = ()=>\x7b
    setTimeout(()=>\x7bwindow.location.reload()\x7d, 500)
\x7d
"""
        download = ""
        if renders[render_id].mp4:
            mp4 = renders[render_id].mp4
            download = f"""
<a
    href="/{mp4}"
    class="hover:underline text-gray-800"
    download
>
    Download MP4
</a>
            """
        return f"""
<html>
<head>
<title>preview for render {render_id}</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
<h1 class="text-2xl">
    Render {render_id}: {renderstate}
</h1>
{download}
<img src="/{latest}">
<script defer>
{reload}
{onload}
</script>
</body>
</html>
    """
    except IndexError:
        return flask.redirect("/static/custom.html")


def recent_renders():
    res = ""
    for render_id in range(len(renders)):
        render = renders[render_id]
        st = render.state
        res += f"""
        <a href="/api/preview?id={render_id}">
            #{render_id} - {st}
        </a>
        <br/>
        """
    return res
