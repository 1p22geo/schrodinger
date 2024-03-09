import flask
import engine
import json
import base64

app = flask.Flask(__name__)


@app.route("/")
def hello_world():
    return flask.redirect("static/index.html")


@app.route("/api/renderpreview")
def renderpreview():
    return engine.renderpreview(
        json.loads(base64.b64decode(flask.request.args.get("state")))
    )
