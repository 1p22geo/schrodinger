import lib


class Deserializer():
    def __init__(self):
        pass

    def ds(self, state):
        dc = state["config"]["domain"]
        config = lib.QuantumConfig(
            1, dc["x"], dc["y"], dc["Nx"], dc["Ny"], dc["Nt"], dc["T_max"]
        )
        potential = None
        match dc['potential']:
            case 'coulomb':
                potential = lib.CoulombPotential(config)
            case 'none':
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
                                sp['sigma'],
                                sp['kx0'],
                                sp['ky0'],
                                sp['x0'],
                                sp['y0'],
                                sp['vx'],
                                sp['vy']
                                )
                            )

        return config, potential, particles
