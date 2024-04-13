import { PARTICLES, POTENTIAL } from "./constants.js";
import { Electron } from "./electron.js";
import { Photon } from "./photon.js";
import { Neutron } from "./neutron.js";
import { Proton } from "./proton.js";
import { CoulombPotential } from "./potential.js";
import { serialize_state } from "./serialization.js";

const state = {
  components: [],
  config: {
    domain: {
      x: 10,
      y: 10,
      Nx: 1000,
      Ny: 1000,
      Nt: 2000,
      T_max: 10,
      interactions: false,
    },
  },
};

let focused_particle = -1;

function switch_sidebar(particleID) {
  if (particleID > state.components.length) {
    throw new Error("Particle ID too high");
  }
  focused_particle = particleID;
  render_sidebar();
}

function render_sidebar() {
  const sidebar = document.querySelector("#sidebar");
  if (focused_particle < 0) {
    sidebar.innerHTML = `
<h1 class="text-xl mb-4">Experiment config</h1>
<form id="config-form" class="flex flex-col gap-2">
  Size of the domain:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${state.config.domain.x}">
      x
  <input type="number" class="mb-4 border w-full" value="${state.config.domain.y}">
  </div>
  Resolution of the domain:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${state.config.domain.Nx}">
      x
  <input type="number" class="mb-4 border w-full" value="${state.config.domain.Ny}">
  </div>

  Length of simulation:
  <input type="number" class="mb-4 border w-full" value="${state.config.domain.T_max}">

  Number of time divisions
  <input type="number" class="mb-4 border w-full" value="${state.config.domain.Nt}">

  [EXPERIMENTAL] [SLOW AND UNOPTIMIZED] [NOT RECOMMENDED] [RADIATION RISK] Inter-particle interactions
  <input type="checkbox" class="mb-4 border" ${state.config.domain.interactions ? "checked" : ""}>

</form>
`;
    const form = document.querySelector(`#config-form`);
    form.onchange = () => {
      state.config.domain.x = parseInt(form.querySelectorAll("input")[0].value);
      state.config.domain.y = parseInt(form.querySelectorAll("input")[1].value);
      state.config.domain.Nx = parseInt(
        form.querySelectorAll("input")[2].value,
      );
      state.config.domain.Ny = parseInt(
        form.querySelectorAll("input")[3].value,
      );
      state.config.domain.T_max = parseInt(
        form.querySelectorAll("input")[4].value,
      );
      state.config.domain.Nt = parseInt(
        form.querySelectorAll("input")[5].value,
      );
      state.config.domain.interactions =
        form.querySelectorAll("input")[6].checked;
      render_data();
    };

    return;
  }

  const particle = state.components[focused_particle];
  switch (particle.__type) {
    case PARTICLES.ELECTRON: {
      sidebar.innerHTML = `
<h1 class="text-xl">Component ${focused_particle}</h1>
<h1 class="mb-4">${particle.__type}</h1>

<form id="config-${focused_particle}" class="flex flex-col gap-2">
<button class="bg-red-600 mb-4 w-24 h-12 text-white self-center grid place-content-center cursor-pointer">DELETE</button>
  Principal quantum number:
  <input type="number" class="mb-4 border" value="${particle.principal_quantum}">
  Azimuthal quantum number:
  <input type="number" class="mb-4 border" value="${particle.azimuthal_quantum}">
  Magnetic quantum number
  <input type="number" class="mb-4 border" value="${particle.magnetic_quantum}">
x0, y0:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.x_center}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.y_center}">
  </div>

</form>
`;
      const form = document.querySelector(`#config-${focused_particle}`);
      form.querySelectorAll("button")[0].onclick = (e) => {
        e.preventDefault();
        state.components.splice(focused_particle, 1);
        render_data();
      };
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
        particle.x_center = parseInt(form.querySelectorAll("input")[3].value);
        particle.y_center = parseInt(form.querySelectorAll("input")[4].value);

        render_data();
      };
      break;
    }
    case PARTICLES.PHOTON: {
      sidebar.innerHTML = `
<h1 class="text-xl">Component ${focused_particle}</h1>
<h1 class="mb-4">${particle.__type}</h1>
<form id="config-${focused_particle}" class="flex flex-col gap-2">
<button class="bg-red-600 mb-4 w-24 h-12 text-white self-center grid place-content-center cursor-pointer">DELETE</button>
&sigma;:
  <input type="number" class="mb-4 border" value="${particle.sigma}">
x0, y0:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.x0}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.y0}">
  </div>
kx0, ky0:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.kx0}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.ky0}">
  </div>
v:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.vx}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.vy}">
  </div>

</form>
`;
      const form = document.querySelector(`#config-${focused_particle}`);
      form.querySelectorAll("button")[0].onclick = (e) => {
        e.preventDefault();
        state.components.splice(focused_particle, 1);
        render_data();
      };
      form.onchange = () => {
        particle.sigma = parseFloat(form.querySelectorAll("input")[0].value);
        particle.x0 = parseFloat(form.querySelectorAll("input")[1].value);
        particle.y0 = parseFloat(form.querySelectorAll("input")[2].value);
        particle.kx0 = parseFloat(form.querySelectorAll("input")[3].value);
        particle.ky0 = parseFloat(form.querySelectorAll("input")[4].value);
        particle.vx = parseFloat(form.querySelectorAll("input")[5].value);
        particle.vy = parseFloat(form.querySelectorAll("input")[6].value);

        render_data();
      };
      break;
    }
    case PARTICLES.NEUTRON: {
      sidebar.innerHTML = `
<h1 class="text-xl">Component ${focused_particle}</h1>
<h1 class="mb-4">${particle.__type}</h1>
<form id="config-${focused_particle}" class="flex flex-col gap-2">
<button class="bg-red-600 mb-4 w-24 h-12 text-white self-center grid place-content-center cursor-pointer">DELETE</button>
spread:
  <input type="number" class="mb-4 border" value="${particle.spread}">
x0, y0:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.x0}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.y0}">
  </div>

</form>
`;
      const form = document.querySelector(`#config-${focused_particle}`);
      form.querySelectorAll("button")[0].onclick = (e) => {
        e.preventDefault();
        state.components.splice(focused_particle, 1);
        render_data();
      };
      form.onchange = () => {
        particle.spread = parseFloat(form.querySelectorAll("input")[0].value);
        particle.x0 = parseFloat(form.querySelectorAll("input")[1].value);
        particle.y0 = parseFloat(form.querySelectorAll("input")[2].value);

        render_data();
      };
      break;
    }
    case PARTICLES.PROTON: {
      sidebar.innerHTML = `
<h1 class="text-xl">Component ${focused_particle}</h1>
<h1 class="mb-4">${particle.__type}</h1>
<form id="config-${focused_particle}" class="flex flex-col gap-2">
<button class="bg-red-600 mb-4 w-24 h-12 text-white self-center grid place-content-center cursor-pointer">DELETE</button>
spread:
  <input type="number" class="mb-4 border" value="${particle.spread}">
x0, y0:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.x0}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.y0}">
  </div>

</form>
`;
      const form = document.querySelector(`#config-${focused_particle}`);
      form.querySelectorAll("button")[0].onclick = (e) => {
        e.preventDefault();
        state.components.splice(focused_particle, 1);
        render_data();
      };
      form.onchange = () => {
        particle.spread = parseFloat(form.querySelectorAll("input")[0].value);
        particle.x0 = parseFloat(form.querySelectorAll("input")[1].value);
        particle.y0 = parseFloat(form.querySelectorAll("input")[2].value);

        render_data();
      };
      break;
    }
    case POTENTIAL.COULOMB: {
      sidebar.innerHTML = `
<h1 class="text-xl">Component ${focused_particle}</h1>
<h1 class="mb-4">${particle.__type}</h1>
<form id="config-${focused_particle}" class="flex flex-col gap-2">
<button class="bg-red-600 mb-4 w-24 h-12 text-white self-center grid place-content-center cursor-pointer">DELETE</button>
charge:
  <input type="number" class="mb-4 border" value="${particle.charge}">
x0, y0:
  <div class="flex flex-row gap-1">
  <input type="number" class="mb-4 border w-full" value="${particle.x_center}">
      ,
  <input type="number" class="mb-4 border w-full" value="${particle.y_center}">
  </div>

</form>
`;
      const form = document.querySelector(`#config-${focused_particle}`);
      form.querySelectorAll("button")[0].onclick = (e) => {
        e.preventDefault();
        state.components.splice(focused_particle, 1);
        render_data();
      };
      form.onchange = () => {
        particle.charge = parseFloat(form.querySelectorAll("input")[0].value);
        particle.x_center = parseFloat(form.querySelectorAll("input")[1].value);
        particle.y_center = parseFloat(form.querySelectorAll("input")[2].value);

        render_data();
      };
      break;
    }

    default:
      break;
  }
}

function render_data() {
  console.log(state);
  document.querySelector("#particles").replaceChildren([]);
  const div = document.createElement("div");
  div.classList.add(
    "cursor-pointer",
    "w-24",
    "h-24",
    "bg-[#101060]",
    "text-white",
    "grid",
    "place-content-center",
  );
  div.id = `config`;
  div.innerText = "FINITE SIMULATED SPACETIME";
  div.onclick = () => {
    switch_sidebar(-1);
  };
  document.querySelector("#particles").appendChild(div);
  state.components.map((p, ix) => {
    const div = document.createElement("div");
    div.classList.add(
      ...p.__style,
      "cursor-pointer",
      "w-24",
      "h-24",
      "grid",
      "place-content-center",
    );
    div.id = `particle-${ix}`;
    div.onclick = () => {
      switch_sidebar(ix);
    };
    div.innerText = p.text;
    document.querySelector("#particles").appendChild(div);
  });
  document.querySelector("#spinner").hidden = false;
  fetch(
    `/api/renderpreview?state=${serialize_state(state)}&req=${parseInt(Math.random() * 10000)}`,
  ).then((res) => {
    res.blob().then((blob) => {
      document
        .querySelector("#main-image-render")
        .setAttribute("src", URL.createObjectURL(blob));
      document.querySelector("#spinner").hidden = true;
      document.querySelector("#eta").innerText =
        `ETA: ${res.headers.get("X-ETA-To-Full-Animation")}`;
    });
  });
}

document.querySelector("#add-electron").onclick = () => {
  state.components.push(new Electron(1, 0, 0, 5.0, 5.0));
  render_data();
};
document.querySelector("#add-photon").onclick = () => {
  state.components.push(new Photon(0.5, 2.0, 2.0, 5.0, 5.0, 0.0, 0.0));
  render_data();
};
document.querySelector("#add-potential").onclick = () => {
  state.components.push(new CoulombPotential(5.0, 5.0, 1));
  render_data();
};
document.querySelector("#add-neutron").onclick = () => {
  state.components.push(new Neutron(5, 5, 3));
  render_data();
};
document.querySelector("#add-proton").onclick = () => {
  state.components.push(new Proton(5, 5, 3));
  render_data();
};

document.querySelector("#reload").onclick = () => {
  render_sidebar();
  render_data();
};

document.querySelector("#render").onclick = () => {
  fetch(
    `/api/render?state=${serialize_state(state)}&req=${parseInt(Math.random() * 10000)}`,
  ).then((res) => {
    res.json().then((json) => {
      window.location.assign(json.preview_url);
    });
  });
};

render_data();
render_sidebar();
