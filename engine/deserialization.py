import lib


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
        config = lib.Config(
            1, dc["x"], dc["y"], dc["Nx"], dc["Ny"], dc["Nt"], dc["T_max"]
        )
        potential = None
        match dc["potential"]:
            case "coulomb":
                potential = lib.CoulombPotential(config)
            case "none":
                potential = lib.EmptyPotential(config)
        serialized_particles = state["particles"]
        particles = []
        for sp in serialized_particles:
            match sp["type"]:
                case "electron":
                    particles.append(
                        lib.Electron(
                            config,
                            potential,
                            sp["principal_quantum"],
                            sp["azimuthal_quantum"],
                            sp["magnetic_quantum"],
                        )
                    )
                case "photon":
                    particles.append(
                        lib.WavePacket(
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
