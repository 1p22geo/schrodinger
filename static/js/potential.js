import { POTENTIAL } from "./constants.js";

export class CoulombPotential {
  constructor(x_center, y_center, charge) {
    this.x_center = x_center;
    this.y_center = y_center;
    this.charge = charge;
    this.__type = POTENTIAL.COULOMB;
    this.text = "COULOMB POTENTIAL"
    this.__style = ["bg-slate-600", "text-white"];
  }
  serialize() {
    return {
      type: POTENTIAL.COULOMB,
      x_center: this.x_center,
      y_center: this.y_center,
      charge: this.charge
    };
  }
}
