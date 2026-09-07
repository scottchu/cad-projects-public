# Drain count handoff

Candidate C3 passed formal review from `2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f` on
`codex/container-desktop-customizer`. User passed independent Top/Bottom drain
checkboxes, then requested count first and pattern second, one item at a time.

DC-DES-01 `/root/drain_count_design` owns BRIEF and DESIGN; baseline manifest
`inputs/baseline.sha256` SHA
`e0304165a054bd228d59d48b024bd9eeed2dfd1f7140f1a202b69411e08390aa`.
Root owns coordination and continuity indexes. Source work starts only after
the design contract is frozen; implementation, critic, validator and formal
reviewer must have distinct identities.

Design is frozen as `inputs/design.sha256`, SHA
`4e4d4ce2ab980e751d12d06fc72d84eb36928903318d29a4362fa8f6c0a630cc`.
DC-IMP-01 `/root/drain_count_implementation` owns source, tests and IMPLEMENTATION.
DC-VAL-PREP `/root/drain_count_validation` prepares probes against git-extracted
baseline files only while implementation runs. Its candidate validation begins
after the source manifest is frozen. Both have four-minute checkpoints;
implementation ceiling ten minutes, preparation ceiling six minutes, with at
most two focused repair cycles. Browser access remains exclusive to root for
the later critic-prescribed checks.

Live private preview <https://mac-mini.duckbill-ionian.ts.net:8453/> currently
serves C3; root Safari reviewed desktop 1440x900 and mobile 390x700. Preserve existing
8448 route, engine lock, all historical CAD/STEP releases and draft PR19.
No pattern implementation, printer action, public hosting or merge in this item.

Candidate C1: `inputs/candidate-01.sha256`, SHA
`bc85262f41c82ab2ae561d91237a4962cb67e3cab5cce12b403530b31a76e748`.
DC-CRIT-01 `/root/drain_count_critic` found an adapter count omission and an
enabled range for malformed count text. DC-IMP-02 is repair cycle one for
those issues. DC-VAL-01 preserves passing compiled evidence bound specifically
to SCAD SHA `517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`;
only unchanged declared inputs may reuse that evidence. Root Safari checks
confirmed the malformed-count range issue. C2 then exposed a disabled exact
input on malformed count; DC-IMP-03 (repair cycle two) separates exact-input
and slider disabled state. Both defects are resolved in C3, including browser
recovery evidence. See CRITIQUE and VALIDATION for dispositions and commands.

Current design revision: `inputs/design-02.sha256`, SHA
`d9537783ac91434d4997c5e0983414f537bf042885957174120d25cee06f8d3a`.
DC-DES-02 resolved exact raw text preservation using text/numeric input and
left the next pattern item unclassified, matching the user's wording.

Final candidate C3: `inputs/candidate-03.sha256`, SHA
`6fa4bb84a83bc859b95b0568d43e34227a5bc2be7f82fe8fb6a2f11796953f57`.
29 Node / 12 Python checks, build, actual mesh counts/ligaments/sidewall/bounds,
source d/R boundaries and byte-identical default seven-hole STL pass.
DC-CRIT-01 `/root/drain_count_critic` owns source and screenshot critique;
DC-VAL-01 `/root/drain_count_validation` owns independent deterministic and
compiled evidence; DC-REV-01 `/root/drain_count_review` owns the formal join.
Physical drainage/strength, slicer, and broader pre-existing UI gates remain
unproven. The user should review count next; pattern follows their gate.

Final joined receipts: IMPLEMENTATION
`610d3c0f33b9e04b2a458bf2fbb570d8193284b55b04eda729e98a7f0c547bd1`;
VALIDATION `ce1f3a71c1abeacf56e7811685aef698c83aa7c898895ae109d113072c5534b5`;
CRITIQUE `1030b59f1253c9b30071936eab0f1f70434dc6fffa2c610dc307b700218dcc51`;
REVIEW `c863bc1334595a6bcad5a543b52bd67397dc5992792082f00d07313d609ccad7`.
Review join manifest SHA
`50ca3ccc31295996104de8244e31ec32faf26753d8ac2eb2303a53801a4e522c`.
Approved for commit to existing draft PR19; no merge or physical acceptance.
