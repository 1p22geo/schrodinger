import flask

app = flask.Flask(__name__)


@app.route("/")
def hello_world():
    return flask.redirect("static/index.html")
