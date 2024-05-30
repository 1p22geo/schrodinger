from libschrodinger.testutils.floateq import floateq
import numpy as np

import libschrodinger.config
import libschrodinger.gauss
import libschrodinger.potential


def test_photon_integral():
    config = libschrodinger.config.Config(1, 20, 20, 1000, 1000, 2000, 10)
    ph = libschrodinger.gauss.WavePacket(config, 0.5, 2, 2, 10, 10, 0, 0)
    res = np.sum((abs(ph.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)


def test_photon_propagate():
    config = libschrodinger.config.Config(1, 20, 20, 1000, 1000, 100, 10)
    potential = libschrodinger.potential.CoulombPotential(config)
    ph = libschrodinger.gauss.WavePacket(config, 0.5, 2, 2, 10, 10, 0, 0)
    res = np.sum((abs(ph.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
    for t in range(config.Nt):
        ph.propagate(potential.V, [], t)
        res = np.sum((abs(ph.psi) ** 2) * (config.dx) * (config.dy))
        assert floateq(res, 1)
