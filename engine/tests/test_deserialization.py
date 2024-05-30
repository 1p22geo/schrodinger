from engine.deserialization import Deserializer

import libschrodinger.electron
import libschrodinger.gauss
import libschrodinger.potential
import libschrodinger.constants


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
                "interactions": False,
            }
        },
        "components": [
            {
                "type":
                libschrodinger.constants.DeserializationConstants.PARTICLES.ELECTRON,
                "principal_quantum": 3,
                "azimuthal_quantum": 2,
                "magnetic_quantum": 1,
                "x_center": 5,
                "y_center": 5,
            },
            {
                "type":
                libschrodinger.constants.DeserializationConstants.PARTICLES.PHOTON,
                "sigma": 0.5,
                "kx0": 1,
                "ky0": 2,
                "x0": 3,
                "y0": 4,
                "vx": 5,
                "vy": 6,
            },
            {
                "type":
                libschrodinger.constants.DeserializationConstants.POTENTIAL.COULOMB,
                "x_center": 5,
                "y_center": 5,
                "charge": 1,
            },
        ],
    }
    config, potentials, particles = Deserializer().ds(state)
    assert config.Lx == 1
    assert config.Ly == 2

    assert config.Nx == 3
    assert config.Ny == 4

    assert config.Nt == 5
    assert config.T_max == 6

    assert isinstance(particles[0], libschrodinger.electron.Electron)
    assert particles[0].principal_quantum == 3
    assert particles[0].azimuthal_quantum == 2
    assert particles[0].magnetic_quantum == 1

    assert isinstance(particles[1], libschrodinger.gauss.WavePacket)
    assert particles[1].vx == 5
    assert particles[1].vy == 6
    # only testing those fields due to access levels

    assert isinstance(potentials[0], libschrodinger.potential.CoulombPotential)

    assert len(particles) == 2
    assert len(potentials) == 1
