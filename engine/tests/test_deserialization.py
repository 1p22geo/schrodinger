from engine.deserialization import Deserializer
from lib.testutils import *
import lib


def test_deserialization_default():
    state = {
        "config": {
            "domain": {
                "x": 1,
                "y": 2,
                "Nx": 3,
                "Ny": 4,
                "Nt": 5,
                "T_max": 6,
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
                "kx0": 1,
                "ky0": 2,
                "x0": 3,
                "y0": 4,
                "vx": 5,
                "vy": 6,
            },
        ],
    }
    config, potential, particles = Deserializer().ds(state)
    assert config.Lx == 1
    assert config.Ly == 2

    assert config.Nx == 3
    assert config.Ny == 4

    assert config.Nt == 5
    assert config.T_max == 6

    assert isinstance(particles[0], lib.Electron)
    assert particles[0].principal_quantum == 3
    assert particles[0].azimuthal_quantum == 2
    assert particles[0].magnetic_quantum == 1

    assert isinstance(particles[1], lib.Photon)
    assert particles[1].vx == 5
    assert particles[1].vy == 6
    # only testing those fields due to access levels

    assert isinstance(potential, lib.CoulombPotential)
