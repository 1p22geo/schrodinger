from lib.testutils.floateq import floateq
import numpy as np

import lib.config
import lib.gauss
import lib.potential


def test_photon_integral():
    config = lib.config.Config(1, 20, 20, 1000, 1000, 2000, 10)
    ph = lib.gauss.WavePacket(config, 0.5, 2, 2, 10, 10, 0, 0)
    res = np.sum((abs(ph.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)


def test_photon_propagate():
    config = lib.config.Config(1, 20, 20, 1000, 1000, 100, 10)
    potential = lib.potential.CoulombPotential(config)
    ph = lib.gauss.WavePacket(config, 0.5, 2, 2, 10, 10, 0, 0)
    res = np.sum((abs(ph.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
    for _ in range(config.Nt):
        ph.propagate(potential.V, [])
        res = np.sum((abs(ph.psi) ** 2) * (config.dx) * (config.dy))
        assert floateq(res, 1)
