# A Python library/web app to simulate quantum-scale physics

Features include (but not limited to):

- create particles in a simulated environment
- create potential fields to account for external forces
- propagate particles (using the titular Schrödinger's equation)
- draw and animate graphs
- ~~access boundary error, core dumped~~ totally not run out of memory
  - on the other hand, Python.

# Library

[examples](./examples/README.md)

## Instalation

```
pip install --upgrade libschrodinger
```

# Web UI

![schreenshot showing app UI where people can create and edit particles](https://github.com/1p22geo/schrodinger/raw/master/static/media/png/screenshot.png)

## Static deployment

[github pages](https://1p22geo.github.io/schrodinger)

[docs](https://1p22geo.github.io/schrodinger/doc/)

Includes everything except for the user experiment engine.
All static files and tutorials included.

## Deploying it yourself

- Install python 3.10 or newer
- First install the required libraries:
  - flask
  - numpy
  - scipy
  - matplotlib
- Install [ffmpeg](https://ffmpeg.org)
- Run the app

```shell
$ python -m flask run -h 0.0.0.0
```

## Running tests

All the dependencies for regular running are needed, together with `pytest`.

Run in your terminal:

```shell
$ python -m pytest
```
