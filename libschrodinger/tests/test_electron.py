from libschrodinger.testutils.floateq import floateq
import numpy as np

import libschrodinger.config
import libschrodinger.electron
import libschrodinger.potential


def test_electron_integral_ground_level():
    config = libschrodinger.config.Config(1, 20, 20, 1000, 1000, 2000, 10)
    el = libschrodinger.electron.Electron(
        config, libschrodinger.potential.CoulombPotential(config), 1, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)


def test_electron_propagate():
    config = libschrodinger.config.Config(1, 20, 20, 1000, 1000, 100, 10)
    potential = libschrodinger.potential.CoulombPotential(config)
    el = libschrodinger.electron.Electron(config, potential, 1, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
    for t in range(config.Nt):
        el.propagate(potential.V, [], t)
        res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
        assert floateq(res, 1)


def test_electron_integral_higher_energy_levels():
    config = libschrodinger.config.Config(1, 20, 20, 1000, 1000, 2000, 10)

    el = libschrodinger.electron.Electron(
        config, libschrodinger.potential.CoulombPotential(config), 2, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = libschrodinger.electron.Electron(
        config, libschrodinger.potential.CoulombPotential(config), 2, 1, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = libschrodinger.electron.Electron(
        config, libschrodinger.potential.CoulombPotential(config), 3, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = libschrodinger.electron.Electron(
        config, libschrodinger.potential.CoulombPotential(config), 3, 2, 1)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
