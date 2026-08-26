# P19 R1 cycle-4 repaired 0.75 mm OPEN-clear independent critique

Decision: **ACCEPT THE EXACT REPAIRED CANDIDATE FOR P19-IMPL-04
SOURCE-FIRST CAD.**

This acceptance covers the frozen analytic YZ motion contract and phone
artifact only. It does not approve generated solids, STEP, slicing, printing,
hand force, friction, backlash, wire safety, heat access, self-locking, or
physical fit/removal.

Owner/role: `/root/p17_optimizer_math_audit`, independent critic. This review
changed no design, CAD source, tests, STEP, PNG, or continuity file.

## Frozen fingerprint

- `REOPTIMIZE_4MM_OPEN_UPRIGHT_INPUT.sha256`: all `7/7` declared content
  entries verified; current manifest SHA-256
  `65923a3ca0861b79e3f36861479f06f80b08c043fec5c790d7065560a48d9143`.
  `sha256sum` also reports the two human-readable `#` header lines as
  improperly formatted; that warning does not affect the seven verified
  content entries.
- `REOPTIMIZED_4MM_OPEN_UPRIGHT_DESIGN.md` SHA-256:
  `36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4`.
- `docs/review/p19-r1-front-edge-short-tail/open-upright-minimum-gate.png`
  SHA-256:
  `b1c04776b585b942a0645383d964a8e9ef1b87e87c8bba2c2b07b25ac3ed59ec`.
- Baseline Git commit: `bcc16305ff112ba814bdf19ad544a5819127e902`.

## Exact candidate independently reconstructed

I used the higher-precision frozen values supplied for independent review:

```text
theta  = 5.000000000000 deg
d      = 4.172814225900 mm
deltaY = 1.552212035894 mm
deltaZ = -0.977677650052 mm
C      = (0,0)
A      = (-13,-9)
```

They produce:

```text
OPEN bottom   = ( 5.000000000000, 10.000000000000)
OPEN diagonal = (20.400000000000, 10.000000000000)
OPEN upright  = (20.400000000000, -9.172814225900)

END bottom    = ( 9.552212035894,  8.022322349948)
END diagonal  = (15.802212035894,  2.272322349948)
END upright   = (22.052212035894, -3.477677650052)
```

OPEN vectors are exactly horizontal then vertical:
`(15.4,0)` and `(0,-19.172814225900)`. END vectors are both
`(6.25,-5.75)`. Rod identities remain `bottom`, `diagonal`, `upright`; all
three straight world paths remain separated and non-crossing.

For the single shared state `u in [0,1]`, I independently evaluated

```text
p_i(u) = OPEN_i + u(END_i-OPEN_i)
alpha_left(u)  = -theta*u
alpha_right(u) = +theta*u
q_s,i(u) = R(-alpha_s(u)) p_i(u)
```

over 1,001 states. Maximum plate-to-world reconstruction residual and maximum
left/right reconstructed-world mismatch were each `7.95e-15 mm`. The two
outer plates therefore use one physical rod state throughout the entire
motion with equal-magnitude opposite rotation. No side remapping, identity
swap, endpoint padding, or manual rail extension is present.

## Six inverse rails and capsule aspects

Independent `200,001`-state centreline integration reproduced:

| outer / rod | centre arc | chord | capsule aspect | minimum crossing |
|---|---:|---:|---:|---:|
| left / bottom | `4.000000000000 mm` | `3.993644065 mm` | `1.963855421687` | `0.753626 deg` at OPEN |
| left / diagonal | `8.012433561030 mm` | `8.001136834 mm` | `2.930706882176` | `6.317446 deg` at END |
| left / upright | `7.864158836934 mm` | `7.856482742 mm` | `2.894978032996` | exact `0 deg` at `u*=0.527104459` |
| right / bottom | `5.944910143797 mm` | `5.938566246 mm` | `2.432508468385` | `0.506324 deg` at OPEN |
| right / diagonal | `10.157688045825 mm` | `10.146318684 mm` | `3.447635673693` | `4.966200 deg` at END |
| right / upright | `4.000000000000 mm` | `3.992179578 mm` | `1.963855421687` | exact `0 deg` at `u*=0.527104459` |

All six physical inverse centre arcs meet `>=4.00 mm`; all complete-capsule
aspects meet `>=1.963855`. Left/bottom and right/upright remain exact active
equalities, so implementation must retain adequate parameter precision and
use an explicit numerical equality tolerance rather than rounding or
shortening either path.

The upright tangent theorem also reproduces. With the repaired upright
`O` and `v=END-OPEN`,

```text
u* = -(O dot v) / |v|^2 = 0.527104459480
```

and `p(u*) dot v = 0`. Both upright inverse rails therefore reach exact zero
instantaneous path/rail crossing at the same shared state. The cycle-4 input
explicitly makes this a reported physical unknown rather than an analytic
blocker when the complete system retains rank `3` and condition `<=15`.
Nevertheless it remains a severe friction, backlash, wedging, and
force-transfer risk; implementation may not turn analytic closure into a
claim of usable clamp force.

## OPEN service, END preload, and reverse removal

Using the exact equal-pitch wire normal, END-derived wire line, and combined
rod/wire radius `4.15 mm`, I reproduced:

| rod | OPEN signed centre distance | OPEN surface clearance | first contact |
|---|---:|---:|---:|
| bottom | `-5.526671 mm` | `+1.376671 mm` | `u=0.846312` |
| diagonal | `+4.900000 mm` | **`+0.750000 mm`** | `u=0.085227` |
| upright | `-9.209869 mm` | `+5.059869 mm` | `u=0.952918` |

Every named rod passes the repaired `>=0.75 mm` OPEN clearance gate. None is
geometrically trapped at the OPEN endpoint. All three END signed distances
are `-3.900000 mm`, preserving the selected `-0.250000 mm` preload proxy.

The reverse shared-u motion gives a plausible **2D nominal release sequence**:
from seated END, upright releases near `u=0.952918`, bottom near `u=0.846312`,
and the limiting diagonal releases near `u=0.085227`; at `u=0`, all three
have positive surface clearance. Thus the analytic endpoint does permit a
nominal wire withdrawal direction rather than leaving one rod permanently
engaged.

That is not physical removal proof. The diagonal remains in nominal contact
through most of the reverse stroke, and the model depends on wire flex while
the exact upright tangency can amplify friction/backlash. Caps, plate faces,
XT60 body, wire bending stiffness, PETG scatter, and the X-separated tool and
withdrawal cone are not represented by this 2D clearance. Actual solids and a
physical test must prove that the seated workpiece can be released without
damage or excessive force.

The short-tail centreline is `7.557267494 mm`. The complete `8 x 8 mm` tool
keepout begins at `Y=28.25 mm`, exactly `0.75 mm` outside the OD55 tangent at
`Y=27.50 mm`; the cup begins `1.75 mm` outside. Physical orientation remains
XT60 head `+Z/up` and short tail/tool `+Y/right`.

## Web, envelope, axle, and closure

Independent `2,001 x 2,001` curve-distance checks reproduced:

- fixed-inner rail-to-rail minimum `4.161275960 mm`;
- left-outer rail-to-rail minimum `4.309451698 mm`;
- right-outer rail-to-rail minimum `3.922382969 mm`;
- fixed/left/right rim webs
  `2.405845086 / 2.555845086 / 2.705845086 mm`;
- conservative axle-guide-to-rod-rail minimum `19.840109320 mm`.

The global estimated 2D web is `2.405845086 mm`, exceeding `2.20 mm` by
`0.205845086 mm`. Plate hierarchy remains
`OD54.4 < OD54.7 < OD55.0`; OD4.15 rod cutters, three OD4x50 rods, six
permanent caps, fixed inners, and opposite rotating outers remain unchanged.
Exact BREP endpoint caps, AF8.15 key corners, fillets, and chamfers remain
future checks.

`C=(0,0)` remains the common rotation datum. `A=(-13,-9)` remains left/behind
and represents one continuous `34.90 mm` X-axis stepped member keyed through
both fixed inners and round-journalled through both outers. It is neither
floating nor a fourth stainless locking rod.

An independent 5,001-state normalized four-contact probe retained rank `3`.
Worst conditions were `7.436100` left and `13.007687` right, both at END.
The candidate therefore passes the `<=15` gate with about `1.9923` margin.
This establishes only nominal local centreline closure, not hand torque,
force, stiffness, friction, or back-drive resistance.

## Phone artifact inspection

The repaired PNG was inspected at original resolution and is suitable for
analytic handoff. It visibly distinguishes:

- OPEN orange and END blue topology, actual wire envelope, XT60 orientation,
  tool keepout, and fixed axle;
- left/right inverse-rail families and their full lengths;
- the exact tangency state and explicit physical-risk boundary;
- the active `0.75 mm` diagonal clearance and condition result;
- one continuous axle through all four plate roles in X section.

No material label collision obscures the topology, service clearance,
tangency warning, rail lengths, or axle architecture.

## Disposition and implementation guards

**ACCEPT FOR P19-IMPL-04 SOURCE-FIRST CAD**, with these mandatory guards:

1. Preserve the exact repaired `theta`, `d`, END translation, C/A, identities,
   plate hierarchy, orientation, and one shared-u opposite-motion law.
2. Carry sufficient precision and enforce the two active `4.00 mm` rail
   equalities with a declared numerical tolerance; do not shorten either
   inverse path.
3. Preserve all three `>=0.75 mm` nominal OPEN surface clearances, all END
   preload targets, and actual-solid web `>=2.20 mm`.
4. Independently test source/export reconstruction parity, full hardware
   collision, caps/keepers, actual wire/XT60 service and X-separated removal
   path before any print recommendation.
5. Preserve rank `3` and condition `<=15`; explicitly retain exact upright
   tangency as a physical force/backlash risk.
6. Make no force, stiffness, friction, backlash, self-lock, heat-safety,
   removal, or physical-acceptance claim without later evidence.

This acceptance authorizes only source-first CAD implementation and its
independent validation pipeline. It does not authorize printing.
