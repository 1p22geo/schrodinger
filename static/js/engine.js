import { Electron } from "./electron.js";
import { serialize_state } from "./serialization.js";

const state = {
  particles: [],
};

function render_data() {
  document
    .querySelector("#main-image-render")
    .setAttribute("src", `/api/renderpreview?state=${serialize_state(state)}`);
}

document.querySelector("#add-electron").onclick = () => {
  state.particles.push(new Electron(1, 0, 0));
  render_data();
};
