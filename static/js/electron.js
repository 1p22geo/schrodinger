export class Electron {
  constructor(principal_quantum, azimuthal_quantum, magnetic_quantum) {
    this.principal_quantum = principal_quantum;
    this.azimuthal_quantum = azimuthal_quantum;
    this.magnetic_quantum = magnetic_quantum;
  }
  serialize() {
    return {
      type: "electron",
      principal_quantum: this.principal_quantum,
      azimuthal_quantum: this.azimuthal_quantum,
      magnetic_quantum: this.magnetic_quantum,
    };
  }
}