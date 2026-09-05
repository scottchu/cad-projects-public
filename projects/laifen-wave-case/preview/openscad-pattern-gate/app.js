(() => {
  "use strict";

  const svg = document.querySelector("#pattern-strip");
  const buttons = [...document.querySelectorAll(".choice")];
  const highlight = document.querySelector("#seam-highlight");
  const kicker = document.querySelector("#state-kicker");
  const summary = document.querySelector("#state-summary");
  const NS = "http://www.w3.org/2000/svg";
  const WIDTH = 720;
  const TOP = 58;
  const BOTTOM = 452;
  const SEAM = 258;
  const AXIAL_PITCH = 4.8;
  const DISPLAY_PITCH = 54;
  const COLORS = Object.freeze({ body: "#d7e8e7", cap: "#e9dcf4" });

  const alternatives = {
    A: {
      label: "A · current OpenSCAD relationship",
      summary: "N34 at crest radius. A 2 mm body blank and 11 mm cap blank form the 13 mm smooth seam band.",
      count: 34,
      blankBelow: 2,
      blankAbove: 11,
      plateau: false,
      density: 8.2,
    },
    B: {
      label: "B · preserved R7 relationship",
      summary: "N33 at valley radius. A 0.18 crest plateau and shared phase carry diamonds to both sides of the seam.",
      count: 33,
      blankBelow: 0,
      blankAbove: 0,
      plateau: true,
      density: 7.9,
    },
  };

  const el = (name, attrs = {}, text = "") => {
    const node = document.createElementNS(NS, name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, String(value)));
    if (text) node.textContent = text;
    return node;
  };

  const addText = (group, x, y, text, attrs = {}) => group.append(el("text", { x, y, fill: "#24323d", "font-size": 14, "font-weight": 750, ...attrs }, text));

  function diamondPath(cx, cy, width, height, plateau) {
    const halfW = width / 2;
    const halfH = height / 2;
    if (!plateau) return `M ${cx} ${cy - halfH} L ${cx + halfW} ${cy} L ${cx} ${cy + halfH} L ${cx - halfW} ${cy} Z`;
    const flat = width * 0.18;
    return `M ${cx - flat} ${cy - halfH} H ${cx + flat} L ${cx + halfW} ${cy} L ${cx + flat} ${cy + halfH} H ${cx - flat} L ${cx - halfW} ${cy} Z`;
  }

  function addPattern(group, option, fromY, toY) {
    const cellW = WIDTH / option.density;
    const halfH = DISPLAY_PITCH / 2;
    for (let y = fromY - DISPLAY_PITCH; y < toY + DISPLAY_PITCH; y += DISPLAY_PITCH) {
      const phase = ((y - SEAM) / DISPLAY_PITCH) * (cellW / 2);
      for (let x = -cellW; x < WIDTH + cellW; x += cellW) {
        group.append(el("path", {
          d: diamondPath(x + phase, y, cellW * .78, halfH * 1.7, option.plateau),
          fill: option.plateau ? "#c497db" : "#83b9b8",
          stroke: option.plateau ? "#6e3f8c" : "#286966",
          "stroke-width": 2,
          "vector-effect": "non-scaling-stroke",
        }));
      }
    }
  }

  function render(choice) {
    const option = alternatives[choice];
    svg.replaceChildren();
    kicker.textContent = option.label;
    summary.textContent = option.summary;
    buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.choice === choice)));

    const capRegion = el("rect", { x: 0, y: TOP, width: WIDTH, height: SEAM - TOP, fill: COLORS.cap, rx: 9, "data-component": "cap" });
    const bodyRegion = el("rect", { x: 0, y: SEAM, width: WIDTH, height: BOTTOM - SEAM, fill: COLORS.body, rx: 9, "data-component": "body" });
    svg.append(capRegion, bodyRegion);
    console.assert(
      capRegion.getAttribute("fill") === COLORS.cap && bodyRegion.getAttribute("fill") === COLORS.body,
      "VFR-03 component background mapping must keep cap above and body below the seam.",
    );
    const pattern = el("g", { "aria-hidden": "true" });
    const bodyStop = SEAM - option.blankBelow * (DISPLAY_PITCH / AXIAL_PITCH);
    const capStart = SEAM + option.blankAbove * (DISPLAY_PITCH / AXIAL_PITCH);
    addPattern(pattern, option, TOP, bodyStop);
    addPattern(pattern, option, capStart, BOTTOM);
    svg.append(pattern);

    if (choice === "A") {
      const blank = el("g", { fill: "#f6fbfb", opacity: .94 });
      blank.append(el("rect", { x: 0, y: bodyStop, width: WIDTH, height: SEAM - bodyStop }));
      blank.append(el("rect", { x: 0, y: SEAM, width: WIDTH, height: capStart - SEAM }));
      svg.append(blank);
      addText(svg, 18, bodyStop - 10, "2 mm body blank", { fill: "#52616c", "font-size": 13 });
      addText(svg, 18, capStart + 20, "11 mm cap blank", { fill: "#52616c", "font-size": 13 });
    }

    svg.append(el("line", { x1: 0, y1: SEAM, x2: WIDTH, y2: SEAM, stroke: highlight.checked ? "#e1643b" : "#536270", "stroke-width": highlight.checked ? 4 : 2, "stroke-dasharray": highlight.checked ? "9 7" : "0" }));
    addText(svg, 18, 82, "CAP · separate piece", { fill: "#4d286a" });
    addText(svg, 18, 432, "BODY · separate piece", { fill: "#1f5957" });
    addText(svg, 520, SEAM - 11, "SEAM DATUM", { fill: "#b24a2c", "font-size": 13, "letter-spacing": 1 });
    addText(svg, 368, 34, choice === "A" ? "N34 · crest-derived · current cutter" : "N33 · valley-derived · 0.18 crest plateau", { fill: "#24323d", "font-size": 15 });
    if (choice === "B") addText(svg, 318, SEAM - 11, "shared phase reaches seam", { fill: "#5a3173", "font-size": 13 });
  }

  buttons.forEach((button) => button.addEventListener("click", () => render(button.dataset.choice)));
  highlight.addEventListener("change", () => render(buttons.find((button) => button.getAttribute("aria-pressed") === "true").dataset.choice));
  render("A");
})();
