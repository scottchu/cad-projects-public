# P20 R3 wire-only 90-degree correction

Date: `2026-08-26`

Status: **FROZEN BOUNDED IMPLEMENTATION**

## Baseline and immutable mechanism

- Baseline HEAD: `9698cf30e9ddb3e576c08179bfdd067446514c67`.
- P20 R2 source SHA-256:
  `1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73`.
- P20 R2 fixed-rail STEP SHA-256:
  `07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c`.
- P20 R2 full-motion STEP SHA-256:
  `715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca`.
- Freeze `C=(0,0)`, `A=(-15,-11)`, physical left/right `+45/-45 deg`, both
  inverse fixed-axle rail loci and their `7.90 mm` cutters, all inner rails,
  and zero white-rod outer rails/apertures.

## Only authorized change

Replace the inherited P19 diagonal workpiece wire occurrence with P18's
accepted exact FRONT-YZ `└` workpiece:

- vertical leg at `Y=-5.0`, tangent at `Z=1.5`, extending toward the XT60;
- exact R6 quarter-circle centered at `(Y=1.0,Z=1.5)`;
- horizontal tail at `Z=-4.5`, from `Y=1.0` to `Y=13.0`, toward `+Y`;
- exact turn `90 deg` / `pi/2 rad`;
- two conductors remain at `X=-3.60/+3.60`;
- XT60 body coordinates remain the identical P18/P19/P20 envelope.

The P20 R3 assembly must delegate to P20 R2 and replace exactly the one
`motion_full_fixed_workpiece_reference` occurrence. It may not copy or redefine
fixed-rod, rail, plate, rod, cap, axle, keeper, or motion math.

## Stop boundary

Generate and validate one full-motion STEP and one full-assembly highlighted
snapshot. Do not run a broad collision sweep, mesh, 3MF, slicing, printing,
physical acceptance, or white-rod outer-rail work.
