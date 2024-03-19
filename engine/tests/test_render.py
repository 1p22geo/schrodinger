from lib.testutils.clearcache import rmtemp
import time
import os

import engine.render


def test_render():
    try:
        rmtemp()
    except:
        print("No static/temp found, continuing...")

    engine.render.queue_render(
        {
            "config": {
                "domain": {
                    "x": 10,
                    "y": 10,
                    "Nx": 1000,
                    "Ny": 1000,
                    "Nt": 10,
                    "T_max": 1,
                    "potential": "coulomb",
                }
            },
            "particles": [
                {
                    "type": "electron",
                    "principal_quantum": 3,
                    "azimuthal_quantum": 2,
                    "magnetic_quantum": 1,
                },
                {
                    "type": "photon",
                    "sigma": 0.5,
                    "kx0": 2,
                    "ky0": 2,
                    "x0": 5,
                    "y0": 5,
                    "vx": 0,
                    "vy": 0,
                },
            ],
        }
    )

    time.sleep(30)
    assert len(os.listdir("static/temp")) == 1
    dirname = os.listdir("static/temp")[0]
    dirname = f"static/temp/{dirname}"
    with open(f"{dirname}/frame_1.png", "rb") as f:
        assert f.readable()
    time.sleep(30)
    with open(f"{dirname}/movie.mp4", "rb") as f:
        assert f.readable()
