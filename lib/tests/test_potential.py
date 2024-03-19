from lib.testutils import floateq
import lib.constants as constants


def test_zero_potential():
    config = constants.Config(1, 20, 20, 2000, 2000, 100, 10)
    pot = constants.EmptyPotential(config)
    for row in pot.V:
        for x in row:
            assert floateq(x, 0)


def test_coulomb_potential():
    config = constants.Config(1, 20, 20, 2000, 2000, 100, 10)
    pot = constants.CoulombPotential(config)
    for row in pot.V:
        for x in row:
            assert x < 0
