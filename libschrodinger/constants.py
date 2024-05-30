NS_IN_DAY = 86_400_000_000_000
"""
nanoseconds in a day, needed for ETA calculations in the engine
"""
NS_IN_HOUR = 3_600_000_000_000
"""
nanoseconds in an hour, needed for ETA calculations in the engine
"""
TEST_TOLERANCE_TRESHOLD = 0.001
"""
the tolerance threshold for libschrodinger.testutils.floateq.floateq()
"""
PLT_FONT = {"fontname": "monospace"}
"""
The fontname dict for Matplotlib
"""


class DeserializationConstants:
    class PARTICLES:
        ELECTRON = "PARTICLES.ELECTRON"
        PHOTON = "PARTICLES.PHOTON"
        NEUTRON = "PARTICLES.NEUTRON"
        PROTON = "PARTICLES.PROTON"

    class POTENTIAL:
        COULOMB = "POTENTIAL.COULOMB"
