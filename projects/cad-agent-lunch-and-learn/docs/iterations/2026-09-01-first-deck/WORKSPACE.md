# W1 workspace metadata receipt

Scope: root workspace metadata only. No HTML, presentation source, frozen design inputs or source-register bytes changed.

Commands run from repository root:

```sh
uv lock --offline
npm install --package-lock-only --ignore-scripts --offline
```

`uv lock --offline` registered virtual package `cad-agent-lunch-and-learn` version `0.1.0`; `npm` completed offline with no audit findings. The inspected diff contains only the new workspace member/link and project records: 6 added lines in `uv.lock` and 5 in `package-lock.json`. No dependency versions changed.

The frozen HTML candidate remains `b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`; its 10 declared inputs verified after the metadata refresh.
