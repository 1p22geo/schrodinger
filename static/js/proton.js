import { PARTICLES } from "./constants.js";

export class Proton {
  constructor(x0, y0, spread) {
    this.x0 = x0;
    this.y0 = y0;
    this.spread = spread;

    this.text = "PROTON";
    this.__type = PARTICLES.PROTON;
    this.__style = ["bg-red-500", "bg-[url('./media/png/icons/proton_smol.jpg')]", "image-bg"];
  }
  serialize() {
    return {
      type: PARTICLES.PROTON,
      x0: this.x0,
      y0: this.y0,
      spread: this.spread,
    };
  }
}
