# OpenSCAD WASM simulator design contract

## 1. Authority and topology

`openscad/laifen_case_customizer_v1.scad` is the sole geometry authority. The
browser supplies parameter overrides and an output selector, then consumes the
STL bytes emitted by OpenSCAD. `openscad/customizer_contract.py` is the existing
independent derivation/constraint oracle for tests. A browser schema adapter may
describe controls, but tests must prove that its names, defaults, ranges, enums,
and derived readouts match the frozen OpenSCAD/Python contracts.

The recovered source SHA-256 is
`b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`;
the focused regression test SHA-256 is
`4e1eea50a2e1fa71b1f420abf2693f2eb96c4ce51d9f4467a39086681dbb5f4e`.
OSC-07 validation SHA-256
`d4323bae7effad0a5f9436fbce78ef933129ddaddfe06a622d73fea23cd12e21`
and evidence-manifest SHA-256
`6e6d01b20f2b29fba73ca4097322f0e880e3c6d970325eb0e528d11a209737f3`
are frozen inputs. They establish the smooth geometry boundary only. Diamond
body and cap each exceeded an independent 60-second native compile ceiling and
remain performance-blocked.

The topology stays two pieces divided at a movable seam. The split continues to
use one canonical input per job: `split_distance_from_top` in distance mode or
`split_percent_from_top` in percentage mode. Thread engagement remains
`thread_pitch * thread_turns`; one- and two-turn configurations are first-class
test cases. No JavaScript primitive, mesh scale, vertex deformation, or CSS
illustration may stand in for compiled geometry.

## 2. Frozen dependency provenance

Use the official prebuilt selected by official `openscad-playground` commit
`012111f06bb6d8dac2b8d30318512494d87d6932`. At that immutable revision,
`libs-config` pins this exact package:

```text
URL: https://files.openscad.org/playground/OpenSCAD-2025.03.25.wasm24456-WebAssembly-web.zip
archive bytes: 2947329
archive SHA-256: 0968af31b9c9b3bba68d9031de1695ccae51c32231a1aab4ef27b18c86379f3b
openscad.js bytes: 124567
openscad.wasm bytes: 9603115
```

This package is the V1 engine dependency. Do not build WASM in this project and
do not substitute a similarly named third-party npm package. The official
`openscad/openscad-wasm` commit
`dc2ff913b4193b1ebfef863da3f7e84f8fbc1e11` remains a recorded upstream source
reference only; it is not claimed to be the build commit for this prebuilt.

A checked-in setup script downloads the pinned URL to a temporary file, verifies
archive byte count and SHA-256 before extraction, rejects redirects outside
`files.openscad.org`, verifies the two expected member names and recorded
uncompressed sizes, and then installs them into a gitignored local dependency
cache. It must use an atomic rename so an interrupted or failed verification
cannot leave a usable-looking partial cache. The 9,603,115-byte WASM binary and
the ZIP are not committed. The dependency lock records the playground commit,
URL, all supplied sizes/hashes, installed file hashes, license provenance, and
setup-script hash. A mismatch stops setup and blocks a candidate.

Use the root-workspace `three@0.176.0` already pinned by `package-lock.json`, with
its matching `STLLoader` and `OrbitControls`. Bundle or copy reviewed modules into
the static artifact; production runtime must make no CDN requests. Dependency
updates require a new candidate fingerprint and the relevant validation gates.

V1 uses a single-thread browser build so static hosting does not depend on
`SharedArrayBuffer` or cross-origin isolation. If the selected official build is
threaded-only, stop and reopen this decision instead of silently weakening the
static-service contract.

## 3. App and asset layout

The future source namespace is `preview/openscad-wasm-simulator/`. Its review
artifact is a self-contained generated directory containing HTML/CSS/modules,
the module worker, pinned Three.js modules, the setup-verified OpenSCAD
loader/WASM cache, and a byte-identical generated copy of the authoritative
`.scad`. The review artifact may be stored under ignored scratch; its manifest
must include every byte, including the uncommitted WASM. The SCAD copy is derived
at build time; its SHA-256 must equal the source SHA-256 or the build fails. It is
never edited as source.

All asset URLs are relative and route-safe. Start the worker with
`new Worker(new URL("./workers/openscad.worker.js", import.meta.url),
{type: "module"})`. The worker's Emscripten `locateFile` callback resolves `.wasm`
and any `.data`/font resources relative to its locked vendor directory, so the
same artifact works at localhost and under `/openscad-simulator/`.

Serve with at least these headers:

```text
Content-Type: application/wasm       # .wasm
Content-Type: text/javascript        # .js/.mjs
Content-Security-Policy: default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; worker-src 'self'; connect-src 'self'; img-src 'self' blob: data:; style-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'
X-Content-Type-Options: nosniff
```

Validation must determine whether the pinned Emscripten build needs any tighter
or additional CSP token. `unsafe-eval`, remote script hosts, and blanket `blob:`
worker permission are not accepted without a recorded upstream requirement and
new review.

## 4. Parameter job contract

The main thread owns the editable form and produces an immutable job snapshot.
The serializer accepts only the frozen allowlist below; numbers must be finite,
inside source bounds, formatted with an ASCII decimal point, and never contain
expressions. Enums are selected from exact literals and serialized as quoted
OpenSCAD strings. The implementation passes arguments as an array to
`callMain`, using `-D`/`name=value` entries and never concatenating a shell or
SCAD program.

```text
device_length device_diameter axial_allowance
outer_diameter body_bore cap_bore minimum_wall floor_thickness end_chamfer
split_mode split_distance_from_top split_percent_from_top
thread_pitch thread_turns thread_clearance thread_depth thread_root_wall
surface_style diamond_axial_pitch diamond_arc_pitch diamond_depth diamond_phase_deg
drainage_mode drain_diameter drain_ring_radius
output_mode
```

`device_diameter` remains a reference-only source parameter and must be labelled
that way. The browser performs cheap constraint checks equivalent to
`customizer_contract.py` before starting a compile, while OpenSCAD assertions
remain final authority. The compiler invocation writes the frozen SCAD bytes to
its virtual filesystem, calls the official module with `--enable=manifold`, the
allowlisted overrides, input path, and output STL path, captures stdout/stderr,
and returns STL bytes plus the exact canonical job record. If the pinned engine
does not support the flag, implementation must record the alternative backend
and reopen the performance/mesh evidence; it must not ignore the flag silently.

V1's job allowlist further fixes `surface_style="smooth"`. The surface selector
shows Smooth as selected and Diamond as a disabled option marked
`pending optimization`; the four diamond parameter controls remain visible,
disabled, and associated with the same explanation. The serializer rejects
`surface_style="diamond"` even if DOM state or a crafted message attempts it,
before worker creation or `callMain`. Disabled diamond values never enter a job
identity. This preserves discoverability of the source capability without
offering a doomed compile, fake surface, or downloadable diamond output.

The result identity is SHA-256 over the SCAD bytes, dependency-lock fingerprint,
canonical parameter JSON, and output mode. The displayed mesh, parameter
readout, and download filename all carry this identity. STL download returns the
same bytes parsed by `STLLoader`, without a second hidden compile.

## 5. Worker state, progress, and cancellation

The state machine is `loading -> ready -> compiling -> parsing -> complete` or
`error/cancelled`. Progress is stage-based and indeterminate while OpenSCAD is
inside `callMain`; the UI must not invent a percentage the engine did not
report. Compiler diagnostics remain visible and copyable without exposing local
filesystem details.

Exactly one compile may run. Each Generate assigns a monotonically increasing
job id. Generate while busy supersedes the old job: terminate its worker, discard
all messages/URLs associated with the old id, create a fresh worker, and run only
the newest complete snapshot. Cancel uses the same termination path and leaves
the last previously successful mesh visibly labelled as not matching current
controls. Object URLs and Three.js geometries/materials are disposed when
replaced. A late result whose job id or result identity is not current is ignored.

Reset restores the published browser preset: all source numeric defaults with
`surface_style="smooth"`. The page must disclose that the authored SCAD default
is diamond, while browser V1 is deliberately smooth-only because diamond failed
the 60-second performance gate. Download always matches the completed smooth
job. Diamond cannot be selected or generated.

## 6. Interface and mobile behavior

Desktop uses a controls column and viewer; narrow screens stack controls,
Generate/progress, viewer, and download with no horizontal page overflow at
360 CSS px. Inputs have persistent labels, units, source ranges, error text tied
with `aria-describedby`, and touch targets at least 44 CSS px. Status uses a
polite live region; compiler failure uses an alert. Generate, Cancel, Reset, and
Download remain reachable by keyboard. Reduced-motion mode removes nonessential
viewer animation, and WebGL failure leaves controls and STL download usable.

The viewer frames bounds from the compiled STL, shows axis/orientation and
output identity, supports orbit/zoom and camera reset, caps device pixel ratio,
and disposes prior resources. It makes no fit, thread-clearance, printability, or
physical-success claim.

## 7. Performance budget

These are acceptance targets measured on the designated desktop and one real or
representative 360–390 px mobile browser over the private static service:

- shell and controls usable within 1.5 s, independent of engine readiness;
- cached worker ready within 15 s desktop and 30 s mobile;
- smooth body or cap STL complete within 15 s desktop and 45 s mobile;
- main-thread input/status tasks stay below 100 ms during compilation;
- after 30 s, show a truthful long-running notice and working Cancel action;
- terminate at 180 s with a recoverable timeout and no downloadable stale file.

Record cold/warm asset transfer, WASM initialization, compile, STL parse, STL
byte size, and peak worker memory when the browser exposes it. The frozen native
diamond timeouts are displayed as the reason the controls are unavailable; V1
must not repeat them in WASM. A future optimized diamond source requires a new
design/candidate and independent native-plus-WASM performance evidence before
those controls can be enabled.

## 8. Validation and delivery

Focused deterministic tests must cover setup URL/size/hash/member rejection and
atomic install; source/schema/default parity; distance
and percentage split equivalence; wide-short proportions; one- and two-turn
engagement; disabled diamond UI and crafted-job rejection; numeric/enum
injection rejection; exact argv construction; result
identity; one-active-job behavior; cancel, supersede and late-result rejection;
reset; error recovery; and source/artifact/download byte parity. A controlled
worker mock may test orchestration, but smooth jobs for all four outputs must run
through the real pinned WASM engine. Diamond must never invoke that engine.

Independent validation inspects generated smooth STL manifold/shell/bounds and
compares selected reference cases with native OpenSCAD output from the same
source and parameters. It confirms body/cap one-component watertight solids,
layout two solids, zero closed volumetric collision, and exact default
39/144/84/219 dimensions. It captures desktop and mobile
default/change/reset/error/cancel
states, checks keyboard and screen-reader status semantics, verifies CSP with no
external requests, and records performance. These checks prove browser
execution and mesh transport only; CAD design acceptance, slicer, printability,
fit, and physical acceptance remain open.

After implementation, critique, validation, and formal review all PASS the same
artifact fingerprint, a delivery worker may copy those exact bytes to
`scratch/presentation/openscad-simulator/`, prove local file/artifact/loopback
byte parity, and add only this mapping:

```text
https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/
  -> http://127.0.0.1:8972/openscad-simulator/
```

The delivery must preserve every existing 8448 mapping and the 3245/3249/8449
services, verify MIME/CSP headers and all loader/worker/WASM subpaths through the
private URL, and capture the actual desktop/mobile delivery surface. MakerWorld,
public hosting, external upload, and website integration remain deferred.
