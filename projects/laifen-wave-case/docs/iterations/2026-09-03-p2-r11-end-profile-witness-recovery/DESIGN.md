# P2 R11 exact witness contract

Frozen partial coverage map SHA-256 `e5d216c2d7c918e10db552e2f09f7f6751c005a00904eb858b5b3c8e8c6018e3`; tests schema/geometry/sensitivity are `321347c8ed6451e3306613661c4fe3b93345ab91b18b7611ae62840972e6aa25`, `6a7cb438a941dd9f6a1f010b4d3aac7cb6a20ccbaf755799229ff7a471f6d9e4`, `eb74b1f9903c32c9682d1fc9a756e8fc39a4bf35fdc9b561c145dd6a9b35eb27`.

Allowed delta is `pairFor` in coverage map only. For each end profile record construct independent raw A/B patches then apply linked normalization: profile A=`chamfer`, B=`rounded_fillet`, each selected end size=1, linked counterpart profile/size synchronized when linked. Assert both derive valid, profiles remain distinct after normalization, and their raw normalized states differ only in declared profile path(s) required by linked coupling. The declared descriptor/SVG target must differ. No special flat witness, generic alternate, validator bypass or test threshold change is allowed.

Validation compares byte diff, runs Phase A/B exact tests, then requires fresh candidate provenance before Phase C. A new cheap failure stops recovery.
