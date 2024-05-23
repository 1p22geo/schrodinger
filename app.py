import flask
import json
import base64

import engine.renderpreview
import engine.render

app = flask.Flask(__name__)


@app.route("/")
def hello_world():
    return flask.redirect("static/index.html")


@app.route("/api/renderpreview")
def renderpreview():
    return engine.renderpreview.renderpreview(
        json.loads(base64.b64decode(flask.request.args.get("state"))),
        flask.request.args.get("mobile") == "true"
    )


@app.route("/api/render")
def queuerender():
    return engine.render.queue_render(
        json.loads(base64.b64decode(flask.request.args.get("state")))
    )


@app.route("/api/preview")
def preview():
    return engine.render.preview_render(int(flask.request.args.get("id")))


@app.route("/api/recent")
def recentrenders():
    return engine.render.recent_renders()
