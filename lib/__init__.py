from lib.electron import Electron
from lib.gauss import WavePacket
from lib.config import QuantumConfig
from lib.potential import (
    CoulombPotential,
    MeanFieldPotential,
    Potential as EmptyPotential,
)
from lib.graphs import GraphDisplay
from lib.figlocation import FigureLocation

NS_IN_DAY = 86_400_000_000_000
NS_IN_HOUR = 3_600_000_000_000
