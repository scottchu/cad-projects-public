# P20 R4 blocked test-print 3MF handoff

Date: `2026-08-27`

## Exact artifacts

- Child candidate fingerprint:
  `e11c3f94b1d4081a4e58db0ec74c76651f234ce97f2e8faa06f59600dc2be871`
  (`14/14`).
- Parent full-CAD fingerprint:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`
  (`30/30`).
- 3MF: `cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.3mf`,
  SHA-256 `cd90dc1afa0c0658981b75a040daa2a8cc91d9addf362ae3bd09420ea4b05135`.
- STEP: `cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.step`,
  SHA-256 `fb1188097e74752522e90dac96996b98c3d1379d42432d09607e62eea47b39e3`.
- Formal review SHA-256:
  `b0ba6fb6db6e88581e484df1ae3e1ea9a566f2e320626d48d147a6b9a23f396f`.

## Required warning

P20 R4 model-only 3MF prepared as a blocked test artifact. It contains 13
printable plastic objects and no rods, XT60, or wire. Mesh/STEP validation
does not waive the XT60 collision or thin-web failures. It has not been
sliced, uploaded, or printed.

## Next action

Wait for user review. Any slicing request must separately resolve the exact
printer/process/filament/tool/support inputs and must continue to label the
current product blockers. Upload and print start require separate fresh
authorization.
