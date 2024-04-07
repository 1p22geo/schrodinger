from lib.testutils.floateq import floateq
import numpy as np

import lib.config
import lib.electron
import lib.potential


def test_electron_integral_ground_level():
    config = lib.config.Config(1, 20, 20, 1000, 1000, 2000, 10)
    el = lib.electron.Electron(
        config, lib.potential.CoulombPotential(config), 1, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)


def test_electron_propagate():
    config = lib.config.Config(1, 20, 20, 1000, 1000, 100, 10)
    potential = lib.potential.CoulombPotential(config)
    el = lib.electron.Electron(config, potential, 1, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
    for _ in range(config.Nt):
        el.propagate(potential.V, [])
        res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
        assert floateq(res, 1)


def test_electron_integral_higher_energy_levels():
    config = lib.config.Config(1, 20, 20, 1000, 1000, 2000, 10)

    el = lib.electron.Electron(
        config, lib.potential.CoulombPotential(config), 2, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = lib.electron.Electron(
        config, lib.potential.CoulombPotential(config), 2, 1, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = lib.electron.Electron(
        config, lib.potential.CoulombPotential(config), 3, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = lib.electron.Electron(
        config, lib.potential.CoulombPotential(config), 3, 2, 1)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
