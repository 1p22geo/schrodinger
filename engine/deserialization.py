import libschrodinger.config
import libschrodinger.potential
import libschrodinger.electron
import libschrodinger.gauss
import libschrodinger.constants
import libschrodinger.quark.baryon


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
        config = libschrodinger.config.Config(
            1,
            dc["x"],
            dc["y"],
            dc["Nx"],
            dc["Ny"],
            dc["Nt"],
            dc["T_max"],
            dc["interactions"],
        )
        serialized_components = state["components"]
        particles = []
        potentials = []
        for sp in serialized_components:
            match sp["type"]:
                case libschrodinger.constants.DeserializationConstants.PARTICLES.ELECTRON:
                    particles.append(
                        libschrodinger.electron.Electron(
                            config,
                            libschrodinger.potential.CoulombPotential(
                                config, sp["x_center"], sp["y_center"]
                            ),
                            sp["principal_quantum"],
                            sp["azimuthal_quantum"],
                            sp["magnetic_quantum"],
                        )
                    )
                case libschrodinger.constants.DeserializationConstants.PARTICLES.PHOTON:
                    particles.append(
                        libschrodinger.gauss.WavePacket(
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
                case libschrodinger.constants.DeserializationConstants.PARTICLES.NEUTRON:
                    particles.append(
                        libschrodinger.quark.baryon.Baryon(
                            config, sp["x0"], sp["y0"], sp["spread"], 0
                        )
                    )
                case libschrodinger.constants.DeserializationConstants.PARTICLES.PROTON:
                    particles.append(
                        libschrodinger.quark.baryon.Baryon(
                            config, sp["x0"], sp["y0"], sp["spread"], 1
                        )
                    )
                    potentials.append(
                        libschrodinger.potential.CoulombPotential(
                            config,
                            x_center=sp["x0"],
                            y_center=sp["y0"],
                            charge=sp["spread"],
                        )
                    )

                case libschrodinger.constants.DeserializationConstants.POTENTIAL.COULOMB:
                    potentials.append(
                        libschrodinger.potential.CoulombPotential(
                            config,
                            x_center=sp["x_center"],
                            y_center=sp["y_center"],
                            charge=sp["charge"],
                        )
                    )

        return config, potentials, particles
