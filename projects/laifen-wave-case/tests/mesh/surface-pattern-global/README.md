# Surface-pattern whole-mesh certifier

This independent validator checks the five exact STL hashes recorded by the
surface-pattern iteration. It uses a C++17 BVH to examine nonadjacent triangle
pairs and every nonincident vertex/edge pair at `1e-6 mm`. It also runs
positive and negative detector fixtures. The compiled binary, STL inputs,
fixtures, and receipt stay under `/tmp`.

From the repository root, using the existing evidence paths:

```sh
certifier_dir="$PWD/projects/laifen-wave-case/tests/mesh/surface-pattern-global"
work_dir=/tmp/surface-pattern-global-replay
mkdir -p "$work_dir"
shasum -a 256 -c "$certifier_dir/CERTIFIER_INPUTS.sha256"
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  "$certifier_dir/mesh_certifier.cpp" -o "$work_dir/mesh_certifier"
uv run python "$certifier_dir/selftest.py" --output-dir "$work_dir"
uv run python "$certifier_dir/run_certification.py" \
  --certifier "$work_dir/mesh_certifier" \
  --fixture-dir "$work_dir" \
  --output "$work_dir/receipt.json" \
  --body /tmp/surface-pattern-validation/diamond-body.stl \
  --cap /tmp/surface-pattern-validation/diamond-cap.stl \
  --assembled /tmp/surface-pattern-validation/diamond-assembled.stl \
  --print-layout /tmp/surface-pattern-validation/diamond-print_layout.stl \
  --wide-print-layout /tmp/surface-pattern-validation/wide-d39-h60-w4.4-t4-both-n17-print_layout.stl
```

If `/tmp/surface-pattern-validation` is unavailable, restore the five named
STLs elsewhere and pass their absolute paths to the same five options. The
runner rejects any byte hash that differs from the recorded artifacts.

This certifies those written meshes at the numeric tolerance. It does not
prove other parameter combinations, browser behavior, CAD/STEP, slicing, or
physical acceptance.
