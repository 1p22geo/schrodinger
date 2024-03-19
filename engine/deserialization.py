import lib.config
import lib.potential
import lib.electron
import lib.gauss

class Deserializer:
    '''
    Simple class for deserializing JSON data from the frontend.
    '''
    def __init__(self):
        pass

    def ds(self, state):
        '''
        Deserialize some data.

        Arguments:
            dict state: the state after
                base64-decoding and json-decoding
        '''
        dc = state["config"]["domain"]
        config = lib.config.Config(
            1, dc["x"], dc["y"], dc["Nx"], dc["Ny"], dc["Nt"], dc["T_max"]
        )
        potential = None
        match dc["potential"]:
            case "coulomb":
                potential = lib.potential.CoulombPotential(config)
            case "none":
                potential = lib.potential.EmptyPotential(config)
        serialized_particles = state["particles"]
        particles = []
        for sp in serialized_particles:
            match sp["type"]:
                case "electron":
                    particles.append(
                        lib.electron.Electron(
                            config,
                            potential,
                            sp["principal_quantum"],
                            sp["azimuthal_quantum"],
                            sp["magnetic_quantum"],
                        )
                    )
                case "photon":
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

        return config, potential, particles
