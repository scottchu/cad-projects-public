# P2 Foundation V1 user gate

**Status:** **PASS** on 2026-09-04  
**Exact user response:** `Yes pass`

## What this V1 would show

One smooth two-piece container whose lower and upper sidewalls have the same outside diameter. The seam sits within the body. The upper piece is a substantial part of the body rather than a small cap. The only closure is a screw. The same model can be viewed assembled or pulled apart axially.

```text
                 +Z / top
              ┌───────────┐
              │ top floor │  F
              │           │
 same OD  ─── │   upper   │  U
              ├───────────┤  splitZ = H - U
              │   lower   │  H - U
              │           │
              │bottom floor│  F
              └───────────┘
                 H total

        assembled                 exploded
       ┌─────────┐             ┌─────────┐ upper
       ├─────────┤                  ↑ gap
       └─────────┘             └─────────┘ lower
```

The diagram establishes identities and relationships only. It is not CAD and does not claim printable threads or fit.

## Fixed for the first implementation

- Lower and upper pieces, coaxial, with one shared outside diameter.
- Body split limited to 25–75% from the top.
- Smooth exterior.
- Screw closure only.
- One-end drain choice only; default bottom.
- Assembled/exploded view.
- All displayed geometry comes from one validated descriptor.

## What you could adjust

- Total height, wall, floor, and outside diameter; the preview reports usable height and minimum clear inside diameter.
- Split by either percent from the top or distance from the top; only one is edited and the other is derived.
- Round or a regular polygon with 3–32 sides.
- Independent flat, chamfer, or rounded top and bottom ends, with the relevant size/radius.
- Screw pitch, one/two/three turns, clearance, depth, and trapezoid/rounded profile; engagement is derived.
- Drain none/top/bottom, count, diameter, and bolt-circle diameter.

## What to inspect

1. Is the lower/upper identity right, with a true body split and equal outside diameter?
2. Is `OD + wall -> clear ID` the right simple V1 relationship, or did you expect clear ID to be the editable input instead?
3. Is one synchronized split control with percent/mm views understandable?
4. Is the round/polygon option still simple enough for V1?
5. Are the independent ends, screw controls, and one-end drain controls the minimum useful set?
6. Is it acceptable to defer every pattern, label, attachment, bayonet, OpenSCAD, and MakerWorld feature until later gates?

## Required response

**PASS or FAIL: Should V1 be implemented exactly as this smooth, same-outside-diameter, body-split screw container with the listed controls and derived values, before adding one feature family at a time?**

## Decision record

The user answered `Yes pass` on 2026-09-04. This approves the fixed and adjustable V1 relationships for the separate bounded preview implementation. It does not approve any deferred feature, CAD, OpenSCAD, export, live-route replacement, or MakerWorld work.
