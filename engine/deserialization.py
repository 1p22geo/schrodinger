import lib.config
import lib.potential
import lib.electron
import lib.gauss
import lib.constants


class Deserializer:
    """
    Simple class for deserializing JSON data from the frontend.
    """

    def __init__(self):
        pass

    def ds(self, state):
        """
        Deserialize some data.

        Arguments:
            dict state: the state after
                base64-decoding and json-decoding
        """
        dc = state["config"]["domain"]
        config = lib.config.Config(
            1, dc["x"], dc["y"], dc["Nx"], dc["Ny"], dc["Nt"], dc["T_max"]
        )
        serialized_components = state["components"]
        particles = []
        potentials = []
        for sp in serialized_components:
            match sp["type"]:
                case lib.constants.DeserializationConstants.PARTICLES.ELECTRON:
                    particles.append(
                        lib.electron.Electron(
                            config,
                            lib.potential.CoulombPotential(
                                config, sp["x_center"], sp["y_center"]
                            ),
                            sp["principal_quantum"],
                            sp["azimuthal_quantum"],
                            sp["magnetic_quantum"],
                        )
                    )
                case lib.constants.DeserializationConstants.PARTICLES.PHOTON:
                    particles.append(
                        lib.gauss.WavePacket(
                            config,
                            sp["sigma"],
                            sp["kx0"],
                            sp["ky0"],
                            sp["x0"],
                            sp["y0"],
                            sp["vx"],
                            sp["vy"],
                        )
                    )
                case lib.constants.DeserializationConstants.POTENTIAL.COULOMB:
                    potentials.append(
                        lib.potential.CoulombPotential(
                            config,
                            x_center=sp["x_center"],
                            y_center=sp["y_center"],
                            charge=sp["charge"],
                        )
                    )

        return config, potentials, particles
