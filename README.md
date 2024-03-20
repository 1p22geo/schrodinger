# A Python script to solve the Schrodinger's equation in a 2D domain.

(spelled that wrong)

## Static deployment

[github pages](https://1p22geo.github.io/schrodinger)

[docs](https://1p22geo.github.io/schrodinger/doc/)

Includes everything except for the customizable experiment engine.
All static files and tutorials included.

## Deploying it yourself

- Install python 3.10 or newer
- First install the required libraries:
  - flask
  - numpy
  - scipy
  - matplotlib
  - shutil
- Install [ffmpeg](https://ffmpeg.org)
- Run the app

```shell
$ python -m flask run
```

## Running tests

All the dependencies for regular running are needed, together with `pytest`.

Run in your terminal:

```shell
$ python -m pytest
```
