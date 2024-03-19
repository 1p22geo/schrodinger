from lib.testutils import floateq
import lib.constants as constants
import numpy as np


def test_electron_integral_ground_level():
    config = constants.Config(1, 20, 20, 1000, 1000, 2000, 10)
    el = constants.Electron(config, constants.CoulombPotential(config), 1, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)


def test_electron_propagate():
    config = constants.Config(1, 20, 20, 1000, 1000, 100, 10)
    potential = constants.CoulombPotential(config)
    el = constants.Electron(config, potential, 1, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
    for _ in range(config.Nt):
        el.propagate(potential.V, [])
        res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
        assert floateq(res, 1)


def test_electron_integral_higher_energy_levels():
    config = constants.Config(1, 20, 20, 1000, 1000, 2000, 10)

    el = constants.Electron(config, constants.CoulombPotential(config), 2, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = constants.Electron(config, constants.CoulombPotential(config), 2, 1, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = constants.Electron(config, constants.CoulombPotential(config), 3, 0, 0)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)

    el = constants.Electron(config, constants.CoulombPotential(config), 3, 2, 1)
    res = np.sum((abs(el.psi) ** 2) * (config.dx) * (config.dy))
    assert floateq(res, 1)
