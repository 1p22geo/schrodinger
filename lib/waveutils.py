import numpy as np


def rollwave(config, wave, vx, vy):
    """
    Move a wave linearily forward by (vx, vy) within experiment coordinates.
    Might not work well with small distances.

    Arguments:
        Config config: the experiment config
        np.array wave: the wave function to roll around.
            shape: (Nx, Ny)
        float vx: the X distance to move the function
        float vy: the Y distance to move the function
    """
    wave = [np.roll(row, int(vy / config.dy * config.dt)) for row in wave]
    wave = np.roll(wave, int(vx / config.dx * config.dt), axis=0)
    """
    TODO: make this work even with smaller v, right now small enough v
        behaves equally to a zero
    """
    return wave
