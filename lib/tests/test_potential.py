from lib.testutils.floateq import floateq

import lib.config
import lib.potential

def test_zero_potential():
    config = lib.config.Config(1, 20, 20, 2000, 2000, 100, 10)
    pot = lib.potential.Potential(config)
    for row in pot.V:
        for x in row:
            assert floateq(x, 0)


def test_coulomb_potential():
    config = lib.config.Config(1, 20, 20, 2000, 2000, 100, 10)
    pot = lib.potential.Potential(config)
    for row in pot.V:
        for x in row:
            assert x <= 0
