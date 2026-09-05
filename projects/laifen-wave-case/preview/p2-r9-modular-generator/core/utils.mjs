export const finite = value => typeof value === "number" && Number.isFinite(value);
export const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
export const rad = degrees => degrees * Math.PI / 180;
export const wrap = value => value - Math.floor(value + .5);
export const deepFreeze = value => {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
};
export const clone = value => structuredClone(value);
export function deepMerge(base, patch) {
  if (Array.isArray(base) || Array.isArray(patch)) return clone(patch ?? base);
  if (!base || typeof base !== "object") return patch === undefined ? base : clone(patch);
  const result = {};
  for (const key of new Set([...Object.keys(base), ...Object.keys(patch || {})])) {
    result[key] = patch && Object.hasOwn(patch, key) ? deepMerge(base[key], patch[key]) : clone(base[key]);
  }
  return result;
}
export function getPath(object, path) { return path.split(".").reduce((value, key) => value?.[key], object); }
export function setPath(object, path, value) {
  const keys = path.split("."); let target = object;
  for (const key of keys.slice(0, -1)) target = target[key];
  target[keys.at(-1)] = value; return object;
}
export const immutable = value => deepFreeze(clone(value));
