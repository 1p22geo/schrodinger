import { PARTICLES } from "./constants.js";

export class Neutron {
  constructor(x0, y0, spread) {
    this.x0 = x0;
    this.y0 = y0;
    this.spread = spread;

    this.text = "NEUTRON"
    this.__type = PARTICLES.NEUTRON;
    this.__style = ["bg-blue-600"];
  }
  serialize() {
    return {
      type: PARTICLES.NEUTRON,
      x0: this.x0,
      y0: this.y0,
      spread: this.spread,
    };
  }
}
