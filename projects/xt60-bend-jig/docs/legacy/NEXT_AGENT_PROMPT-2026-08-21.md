# Prompt for the next Codex task

Continue the XT60 bend-jig project in:

`/Users/scottchu/Projects/personal/3d-print/design/xt60-bend-jig`

You are taking over an active parametric CAD prototype. Read `HANDOFF.md` in
full before doing anything, then inspect the authoritative P13 source, design
brief, tests, production 3MF provenance, and current Git status.

The user is about to PETG-print:

`cad/p13_four_plate_three_rod/p13_print_kit.3mf`

Your immediate job is **physical-test follow-up**, not speculative redesign.
Wait for the user's print observations. Help them identify assembly order and
record actual fit, wire retention, binding, cap retention, soldering access,
PETG behaviour, wire damage, final cooled bend angle, and springback.

Critical design intent:

- clamp/form only the two insulated wires, not the XT60 plastic body;
- fixed 90-degree wire path;
- three purchased `Ø4 x 50 mm` stainless rods;
- four circular plates and one rotary input;
- all three rods have equal scalar travel along different guide directions;
- current final geometric preload is the named parameter
  `wire_preload = 0.25 mm` over `22°..27°`;
- the architecture and all generated outputs must remain parametric.

Treat the current CAD evidence as CAD-only acceptance. It does not prove actual
force, wire insulation safety, printed fit, PETG stiffness/creep/heat response,
or springback. Do not modify the CAD before the physical report unless the user
shows an obvious assembly impossibility.

If the physical test says the hold is too loose or too tight, first evaluate a
minimal `wire_preload` retune within the existing `0.00..0.40 mm` range. Do not
change architecture casually. For any material change, use an explicit loop:

1. architect/specify invariants and acceptance criteria;
2. delegate implementation;
3. delegate independent critic/review;
4. delegate independent tests and actual-solid/export validation;
5. resolve findings and repeat until no material findings remain;
6. regenerate dependent STEP/3MF/evidence from source with `uv`;
7. report CAD evidence separately from remaining physical tests.

Preserve the user's working tree. The parent repository currently sees the
project directory as untracked; do not create a clean worktree that omits these
files, and do not delete older versions, caches, or artifacts unless explicitly
asked after a scoped dry run.

Start by telling the user exactly which physical observations you need from the
print, then wait. Do not claim production readiness.
