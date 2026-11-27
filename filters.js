(() => {
  const form = document.getElementById("filters");
  const entries = Array.from(document.querySelectorAll(".index-list .writing-item"));
  const count = document.getElementById("result-count");
  const empty = document.getElementById("empty");
  const controls = Array.from(form.elements).filter(control => control.name);

  function readAddress() {
    const params = new URLSearchParams(location.search);
    for (const input of controls) input.value = params.get(input.name) || "";
  }

  function filter(save) {
    const {type, area, from, to} = form.elements;
    const invalidRange = from.value && to.value && from.value > to.value;
    let visible = 0;
    for (const item of entries) {
      const data = item.dataset;
      const matches = !invalidRange
        && (!type.value || type.value === data.type)
        && (!area.value || data.areas.split(" ").includes(area.value))
        && (!from.value || from.value <= data.date)
        && (!to.value || data.date <= to.value);
      item.hidden = !matches;
      if (matches) visible += 1;
    }
    count.textContent = invalidRange ? "The end date must be on or after the start date."
      : visible + (visible === 1 ? " work" : " works");
    to.setAttribute("aria-invalid", invalidRange ? "true" : "false");
    empty.hidden = visible > 0 || Boolean(invalidRange);
    if (save && ["http:", "https:"].includes(location.protocol)) {
      const url = new URL(location.href);
      for (const input of controls) {
        if (input.value) url.searchParams.set(input.name, input.value);
        else url.searchParams.delete(input.name);
      }
      history.replaceState(null, "", url);
    }
  }

  form.addEventListener("change", () => filter(true));
  form.addEventListener("submit", event => { event.preventDefault(); filter(true); });
  form.addEventListener("reset", event => {
    event.preventDefault();
    for (const input of controls) input.value = "";
    filter(true);
  });
  window.addEventListener("popstate", () => { readAddress(); filter(false); });
  readAddress();
  filter(false);
  form.hidden = false;
})();
