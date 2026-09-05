# P2 R13 renderer-fidelity recovery handoff

**Status:** design complete; implementation has not started.

DES-GCS-R13-01 froze a recovery contract against R12 candidate `51727da73c72db6e391f4f83014a54076dc2ffbdc5bc617f753c72a8fc1a2221`. R12 pure schema/derive evidence remains PASS; its visual candidate remains failed/blocked. R13 uses a new preview namespace and keeps the R12 core and all existing candidate/evidence bytes read-only.

The implementation owner must first verify `inputs/frozen-inputs.sha256` and the nested R12 manifests, then prove the existing descriptor supplies every row in the 84-field oracle. A descriptor gap is a hard stop, not permission to edit core. Cheap canonical SVG/DOM and family-alias gates must pass before any browser capture.

Implementation is bounded to the paths in `BRIEF.md`, one initial attempt plus two focused repair cycles. Independent validator and critic must both PASS the same frozen candidate before formal review. There is no delivery or live-route authorization.

Frozen input manifest: `inputs/frozen-inputs.sha256`, 41 entries, SHA-256/design fingerprint `3a322e3d836cb07fa44600feba4b27ada6c91c07e90015b0184edcb62a3fc42d`. The manifest, nested R12 candidate/evidence manifests, and the exact ordered 84-field oracle all verified before handoff.
