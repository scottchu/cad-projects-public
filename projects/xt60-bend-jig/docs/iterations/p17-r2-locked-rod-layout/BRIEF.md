# P17-D13 locked rod-layout contract

Status: **DESIGN CONTRACT FROZEN; IMPLEMENTATION BLOCKED**.

This remains P17 R2. The user locked one numeric placement change; the design
role did not optimize, repair, mirror, or reinterpret it.

## Baseline

- I10-R1 checkpoint manifest:
  `/tmp/p17-i10-r1-independent-gate-manifest.txt`.
- Manifest/fingerprint SHA-256:
  `5443e39e3b82bbbc2f6e3ed8dd6c2487a69035c263d44128a47f31ddab509d93`.
- I10 source/test hashes recorded by the baseline owner:
  `0d66dd9b0668c976750036c03bb8b8886a04df2d557ddee4330e933072161060`
  and
  `e1806f15ffb5b92afcd92f665e501ed58632bddfc991733d0224c431f2286895`.
- The manifest file itself was rehashed exactly in this worktree. Its historical
  `24/24` checkpoint payload is no longer fully materialized here, so this
  iteration freezes the baseline owner’s exact coordinate receipt rather than
  claiming a live 24-row artifact revalidation.

## User-locked change

Apply exactly one common placement delta to every state of all three stainless
rods, their three fixed-inner straight tracks, and their six inverse-derived
outer rails:

```text
DY = +16.1869657526 mm
DZ = +10.2949747468 mm
```

No Y- or Z-component may be adjusted. Change the fixed purple axle only from
`A=(-29,17)` to `A=(-29,12)`. Keep `C=(3,12)`.

Freeze the I10 workpiece independently of the rod delta: XT60 body
`(-6.5,22.5)`, bend `B=(-0.5,3.5)`, vertical wire `Y=-6.5`, horizontal wire
`Z=-2.5`, and extraction endpoint `Y=17.265`.

The relative OPEN/contact/END triangles, rod identities, common
`10.5852813742 mm` stroke, `theta=24u deg`, OD4x50 rods, six permanent caps,
four plate envelopes, slot widths, part topology and opposite outer rotation
remain unchanged.

## Exact outcome and disposition

The translated END rod Z coordinates are `19.7949747468`, `12.3100505063`,
and `3.8949747468`; their centroid is `11.99999999997 mm`, satisfying the
locked `Z=12` target.

All nine rod tracks are mathematically constructible inside the existing
plates. The limiting analytic rail/feature web is `3.632336547 mm`, above the
`2.20 mm` gate, and the limiting plate boundary web is `3.294595306 mm` at the
fixed inner hex bore.

Implementation is nevertheless blocked because the locked rod-only
translation breaks the product interface:

1. the bottom rod OPEN center `(-4.7983156216,19.7949747468)` lies inside the
   frozen XT60 body YZ rectangle `Y=-10.55..-2.45`, `Z=12.25..32.75`; an OD4
   rod therefore intersects/loads the XT60 body, with 2D signed clearance
   `-2.000 mm`;
2. the same OPEN center is only `1.7016843784 mm` from the frozen vertical-wire
   centerline at `Y=-6.5`, less than the `4.15 mm` rod-plus-wire radii, so OPEN
   also has `2.4483156216 mm` radial overlap with the wire envelope;
3. END no longer forms the two wire straights: bottom-to-vertical surface gap
   is `8.136965753 mm` and upright-to-horizontal gap is `2.244974747 mm`, so
   the prior three-point contact/preload contract is lost;
4. the locked translation also destroys the user-approved I10 rail balance:
   full left/right ratios become `1.859285`, `1.605235`, and `3.071372`; the
   minimum contact crossing angle is only `4.387453 deg`. This fourth item is
   a force/path-balance diagnostic, not a hard collision or physical-force
   proof; items 1–3 are hard geometric interface failures.

No implementation, CAD/export acceptance, force, self-lock, fit or physical
claim is authorized from this blocked contract. The next step requires an
explicit user scope decision; the design agent must not silently change the
locked coordinates.
