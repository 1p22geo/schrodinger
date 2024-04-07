export function serialize_state(state) {
  let components = [];
  state.components.forEach((p) => {
    components.push(p.serialize());
  });
  return btoa(
    JSON.stringify({
      components,
      config: state.config,
    }),
  );
}
