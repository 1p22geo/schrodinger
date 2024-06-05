import numpy as np

import libschrodinger.config


def rollwave(
    config: libschrodinger.config.Config, wave: np.ndarray, vx: float, vy: float
):
    """
    Move a wave linearily forward by `(vx, vy)` within experiment coordinates.
    Might not work well with small distances.

    Parameters
    ----------
    - `config: libschrodinger.config.Config`: the domain config
    - `wave: np.ndarray`: the wave to move, an array of shape `(Nx, Ny)`
    - `vx: float`: the X velocity (will be normalized, taking into account dx and dt)
    - `vy: float`: the Y velocity (will be normalized, taking into account dy and dt)

    """
    wave = [np.roll(row, int(vy / config.dy * config.dt)) for row in wave]
    wave = np.roll(wave, int(vx / config.dx * config.dt), axis=0)
    """
    TODO: make this work even with smaller v, right now small enough v
        behaves equally to a zero
    """
    return wave
