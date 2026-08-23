# Q3-R0 candidate reference

Q3-R0 is preserved only as a candidate/reference for the one-identical-sector, quantity-three seam direction. This folder includes three source modules, one focused test, three wrapper generators, and four STEP/3MF files under `written/`.

It is not current, CAD accepted for restart, slicer accepted, or physically accepted. Do not regenerate these historical artifacts merely to match their hashes. Future work must move adopted source into a new restart namespace.

## Recovery status

This packet is frozen provenance and is not runnable or generatable in place. Exact recoverable legacy routes are:

- `legacy/source-project/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec.py`
- `legacy/source-project/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry.py`
- `legacy/source-project/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_export.py`
- `legacy/source-project/tests/test_p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview.py`
- `legacy/source-project/models/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview/` for the wrapper generators only

Do not generate into `references/q3-r0/`. If KAGE-EXP-001 authors a coupon, it must copy the minimum adopted concepts into a newly named restart namespace, keep Q3-R0 unchanged, add its own focused test, and generate explicitly named new outputs outside this frozen packet.
