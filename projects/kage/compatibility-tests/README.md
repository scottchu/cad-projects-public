# Historical compatibility tests

This directory is non-normative. Its tests exercise the installed historical Kage simulator/optics compatibility runtime and can detect migration breakage, but passing them does not make their commodity-quartz, no-gearing, non-hollow-center `reference-final` architecture current, accepted, or suitable as the restart CAD contract.

Run them only when that compatibility surface is relevant:

```sh
uv run --package kage pytest projects/kage/compatibility-tests
```

Normal migration acceptance runs only `projects/kage/tests/`. Historical CAD suites remain under `legacy/source-project/tests/` and selected frozen reference tests remain under `references/`; neither is silently included here.
