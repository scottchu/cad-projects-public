# Printing profiles — main-port documentation contract

Shared FDM rules describe load-relative orientation and manufacturing concerns;
each project owns editable settings, per-part choices and immutable run evidence.
Markdown is descriptive, not an executable slicer preset. Pending fields are not
guessed defaults; actual slicer settings/overrides and physical outcomes remain
separate from intentions and available workshop equipment.

The shared rules, template and Kage profile are byte-identical to the prior local
documentation implementation. Main's XT60 authority is P19 R1, so its new profile
describes four plates, axle/keepers, six caps and three purchased rods, with P19
fit/service/force risks. It does not import unmerged newer mechanisms, settings,
collision claims or handoff links. Historical coupon results remain role/process
limited, not current full-assembly acceptance.

Only printing-profile policy additions are ported; earlier local workflow or
geometry changes are excluded. Existing frozen project contracts remain exact.
Independent main-specific review is required even where earlier core review
exists. No new design version or printing authority follows from this PR.
