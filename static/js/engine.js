import { PARTICLES } from "./constants.js";
import { Electron } from "./electron.js";
import { serialize_state } from "./serialization.js";

const state = {
  particles: [],
};

let focused_particle = -1;

function switch_sidebar(particleID) {
  if (particleID > state.particles.length) {
    throw new Error("Particle ID too high");
  }
  focused_particle = particleID;
  render_sidebar();
}

function render_sidebar() {
  const sidebar = document.querySelector("#sidebar");
  if (focused_particle < 0) {
    sidebar.innerHTML = `
<h1>Experiment config</h1>
<h2>not implemented yet</h2>
`;
    return;
  }

  const particle = state.particles[focused_particle];
  switch (particle.__type) {
    case PARTICLES.ELECTRON: {
      sidebar.innerHTML = `
<h1>Particle ${focused_particle}</h1>
<h1>${particle.__type}</h1>
<form id="config-${focused_particle}" class="flex flex-col gap-4">
  Principal quantum number:
  <input type="number" class="mb-4 border" value="${particle.principal_quantum}">
  Azimuthal quantum number:
  <input type="number" class="mb-4 border" value="${particle.azimuthal_quantum}">
  Magnetic quantum number
  <input type="number" class="mb-4 border" value="${particle.magnetic_quantum}">
</form>
`;
      const form = document.querySelector(`#config-${focused_particle}`);
      form.onchange = () => {
        particle.principal_quantum = parseInt(
          form.querySelectorAll("input")[0].value,
        );
        particle.azimuthal_quantum = parseInt(
          form.querySelectorAll("input")[1].value,
        );
        particle.magnetic_quantum = parseInt(
          form.querySelectorAll("input")[2].value,
        );
        render_data();
      };
      break;
    }

    default:
      break;
  }
}

function render_data() {
  document.querySelector("#particles").replaceChildren([]);
  const div = document.createElement("div");
  div.classList.add(
    "cursor-pointer",
    "w-24",
    "h-24",
    "bg-[#101060]",
    "text-white",
  );
  div.id = `config`;
  div.innerText = "FINITE SIMULATED SPACETIME";
  div.onclick = () => {
    switch_sidebar(-1);
  };
  document.querySelector("#particles").appendChild(div);
  state.particles.map((p, ix) => {
    console.log(p);
    const div = document.createElement("div");
    div.classList.add("cursor-pointer", "w-24", "h-24", "bg-green-300");
    div.id = `particle-${ix}`;
    div.onclick = () => {
      switch_sidebar(ix);
    };
    div.innerText = p.__type;
    document.querySelector("#particles").appendChild(div);
  });
  document
    .querySelector("#main-image-render")
    .setAttribute("src", `/api/renderpreview?state=${serialize_state(state)}`);
}

document.querySelector("#add-electron").onclick = () => {
  state.particles.push(new Electron(1, 0, 0));
  render_data();
};

render_data();
render_sidebar();
