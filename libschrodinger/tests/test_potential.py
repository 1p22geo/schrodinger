from libschrodinger.testutils.floateq import floateq

import libschrodinger.config
import libschrodinger.potential


def test_zero_potential():
    config = libschrodinger.config.Config(1, 20, 20, 2000, 2000, 100, 10)
    pot = libschrodinger.potential.Potential(config)
    for row in pot.V:
        for x in row:
            assert floateq(x, 0)


def test_coulomb_potential():
    config = libschrodinger.config.Config(1, 20, 20, 2000, 2000, 100, 10)
    pot = libschrodinger.potential.Potential(config)
    for row in pot.V:
        for x in row:
            assert x <= 0
