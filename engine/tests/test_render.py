from lib.testutils.clearcache import rmtemp
from lib.testutils.asserts import assert_file_exists
import lib.constants
import time
import os

import engine.render


def test_render():
    try:
        rmtemp()
    except OSError:
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
                    "interactions": False,
                }
            },
            "components": [
                {
                    "type": lib.constants.DeserializationConstants.PARTICLES.ELECTRON,
                    "principal_quantum": 3,
                    "azimuthal_quantum": 2,
                    "magnetic_quantum": 1,
                    "x_center": 5,
                    "y_center": 5,
                },
                {
                    "type": lib.constants.DeserializationConstants.PARTICLES.PHOTON,
                    "sigma": 0.5,
                    "kx0": 2,
                    "ky0": 2,
                    "x0": 5,
                    "y0": 5,
                    "vx": 0,
                    "vy": 0,
                },
                {
                    "type": lib.constants.DeserializationConstants.POTENTIAL.COULOMB,
                    "x_center": 5,
                    "y_center": 5,
                    "charge": 1,
                },
            ],
        }
    )

    time.sleep(30)
    assert len(os.listdir("static/temp")) == 1
    dirname = os.listdir("static/temp")[0]
    dirname = f"static/temp/{dirname}"
    assert assert_file_exists(f"{dirname}/frame_1.png", 30)
    assert assert_file_exists(f"{dirname}/movie.mp4", 90)
