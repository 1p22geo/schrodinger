export function serialize_state(state) {
  let particle_state = [];
  state.particles.forEach((p) => {
    particle_state.push(p.serialize());
  });
  return btoa(
    JSON.stringify({
      particles: particle_state,
      config: state.config,
    }),
  );
}
