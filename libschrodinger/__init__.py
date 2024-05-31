"""
## Main library package
for 1p22geo/schrodinger

---

Use links on the left for all functions and classes
of the main package.

Subpackages available:
---
`libschrodinger.quark` - package related to quarks and particles composed of quarks
"""
import libschrodinger.quark.hadron
import libschrodinger.quark.baryon
import libschrodinger.quark.meson
import libschrodinger.quark.color
import libschrodinger.quark.quark
import libschrodinger.waveutils
import libschrodinger.potential
import libschrodinger.particle
import libschrodinger.interaction
import libschrodinger.graphs
import libschrodinger.constants
import libschrodinger.config
import libschrodinger.electron
import libschrodinger.figlocation
import libschrodinger.gauss
from importlib.metadata import version
__version__ = version('libschrodinger')
print(f"Starting libschrodinger v{__version__}")
