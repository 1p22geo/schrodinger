import { PARTICLES } from "./constants.js";

export class Electron {
  constructor(
    principal_quantum,
    azimuthal_quantum,
    magnetic_quantum,
    x_center,
    y_center,
  ) {
    this.principal_quantum = principal_quantum;
    this.azimuthal_quantum = azimuthal_quantum;
    this.magnetic_quantum = magnetic_quantum;
    this.x_center = x_center;
    this.y_center = y_center;
    this.text = "ELECTRON";
    this.__type = PARTICLES.ELECTRON;
    this.__style = ["bg-green-300"];
  }
  serialize() {
    return {
      type: PARTICLES.ELECTRON,
      principal_quantum: this.principal_quantum,
      azimuthal_quantum: this.azimuthal_quantum,
      magnetic_quantum: this.magnetic_quantum,
      x_center: this.x_center,
      y_center: this.y_center,
    };
  }
}
