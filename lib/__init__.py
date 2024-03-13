from lib.electron import Electron
from lib.gauss import WavePacket
from lib.gauss import WavePacket as Photon  # alias for web UI engine
from lib.config import Config
from lib.potential import (
    CoulombPotential,
    MeanFieldPotential,
    Potential as EmptyPotential,
)
from lib.graphs import GraphDisplay
from lib.figlocation import FigureLocation
import lib.waveutils as waveutils

NS_IN_DAY = 86_400_000_000_000
NS_IN_HOUR = 3_600_000_000_000
TEST_TOLERANCE_TRESHOLD = 0.001
