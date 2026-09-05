export function readoutRows(descriptor) {
  if (!descriptor) throw new TypeError("A valid descriptor is required for readout.");
  const d = descriptor;
  return [
    ["Clear ID", `${d.ID.toFixed(2)} mm`], ["Usable height", `${d.usableHeight.toFixed(2)} mm`],
    ["Lower / upper", `${d.lowerLength.toFixed(2)} / ${d.upperLength.toFixed(2)} mm`],
    ["Split", `${d.splitPercent.toFixed(2)}% / ${d.U.toFixed(2)} mm from top`],
    ["Engagement", `${d.screw.engagement.toFixed(2)} mm`], ["Diametral clearance", `${d.screw.diametralClearance.toFixed(2)} mm`],
    ["Residual thread wall", `${d.screw.residualThreadWall.toFixed(2)} mm`],
    ["Drain feasibility", d.drains.location === "none" ? "No drain selected" : `${d.drains.count} hole${d.drains.count === 1 ? "" : "s"} on ${d.drains.location}`],
  ];
}
