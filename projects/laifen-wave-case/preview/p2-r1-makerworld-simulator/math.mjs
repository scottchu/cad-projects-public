// Pure axial accounting and global-Z skin field for the intent preview.
export const DEFAULTS = Object.freeze({
  deviceLength: 208, axialAllowance: 5, floor: 3, outerDiameter: 39,
  bodyBore: 30, upperBore: 31, threadPitch: 2, engagement: 6,
  cavityOverlap: 5, splitFromTop: 84, pattern: "blunt-diamond",
  skinPitch: 4.8, skinCount: 33, skinHeight: 0.45, plateauHalf: 0.18,
});

export const clamp = (n, lo, hi) => Math.min(hi, Math.max(lo, n));
export const wrap = (x) => x - Math.floor(x + 0.5);
export const splitPercentBounds = (H) => ({ min: 100 * 50 / H, max: 100 * 169 / H });
export const splitFromPercent = (percent, H) => H * percent / 100;
export const percentFromSplit = (S, H) => 100 * S / H;
// A three-decimal displayed endpoint can differ by up to .0016 mm at H=311.
// Accept only that display rounding, never a real outside-range percentage.
export function canonicalSplitFromPercent(percent, H) {
  const raw = splitFromPercent(percent, H), bounds = splitPercentBounds(H);
  const roundingToleranceMm = 0.002;
  if (percent >= bounds.min - 0.0005 && raw >= 50 - roundingToleranceMm && raw <= 50) return 50;
  if (percent <= bounds.max + 0.0005 && raw <= 169 + roundingToleranceMm && raw >= 169) return 169;
  return raw;
}

export function deriveSimulator(values = {}) {
  const p = { ...DEFAULTS, ...values };
  const C = p.deviceLength + p.axialAllowance;
  const H = C + 2 * p.floor;
  const S = p.splitFromTop;
  const U = S - p.floor;
  const B = C - U + p.cavityOverlap;
  const penetration = p.engagement + 1.5 * p.threadPitch;
  const seamZ = H - S;
  const lowerOuter = B + p.floor + (penetration - p.cavityOverlap);
  const upperOuter = U + p.floor;
  const finite = Object.values(p).every((v) => typeof v !== "number" || Number.isFinite(v));
  const errors = [];
  if (!finite) errors.push("A numeric value is not finite.");
  if (S < 50 || S > 169) errors.push("Split must remain between 50 and 169 mm from the closed top.");
  if (p.axialAllowance < 3) errors.push("Axial allowance is below the 3 mm reference.");
  if (p.engagement < 5 || p.engagement > 6) errors.push("Effective thread engagement must be 5–6 mm.");
  // The preview's device diameter is a reference value, separate from its length.
  const deviceDiameter = Number.isFinite(values.deviceDiameter) ? values.deviceDiameter : 29;
  const lowerGap = (p.bodyBore - deviceDiameter) / 2;
  const upperGap = (p.upperBore - deviceDiameter) / 2;
  if (lowerGap < 0 || upperGap < 0) errors.push("A nominal radial reference gap is negative.");
  const residualWall = p.outerDiameter / 2 - p.skinHeight - p.upperBore / 2;
  const warnings = ["Visual model only: consult CAD before treating any readout as a wall or thread claim."];
  if (U < 60 || B < 60) warnings.push("One cavity-accounting length is below 60 mm.");
  if (residualWall < 1.8) warnings.push("Visual skin residual-wall estimate is below 1.8 mm.");
  return {
    ...p, deviceDiameter, C, H, S, percent: percentFromSplit(S, H), U, B, penetration, seamZ,
    upperOuter, lowerOuter, lowerInterval: [0, seamZ + penetration], upperInterval: [seamZ, H],
    threadBand: [seamZ, seamZ + penetration], effectiveBand: [seamZ + 1.5, seamZ + 1.5 + p.engagement],
    lowerGap, upperGap, residualWall, errors, warnings, valid: errors.length === 0,
  };
}

// Every branch takes assembled zGlobal; no piece-local origin is available here.
export function patternRelief(pattern, theta, zGlobal, p = DEFAULTS) {
  if (pattern === "smooth") return 0;
  if (pattern === "blunt-diamond") {
    const u = p.skinCount * theta / (2 * Math.PI);
    const v = zGlobal / p.skinPitch;
    const diamond = clamp((0.5 - Math.max(Math.abs(wrap(u + v)), Math.abs(wrap(u - v)))) / (0.5 - p.plateauHalf), 0, 1);
    return p.skinHeight * diamond;
  }
  if (pattern === "shallow-helix") return 0.30 * (0.5 + 0.5 * Math.sin(12 * theta + (2 * Math.PI * zGlobal / 24)));
  if (pattern === "wave-flutes") return 0.30 * (0.5 + 0.5 * Math.cos(12 * theta + 0.22 * Math.sin(2 * Math.PI * zGlobal / 48)));
  return 0;
}
