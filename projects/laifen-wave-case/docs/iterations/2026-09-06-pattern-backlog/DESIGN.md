# PB-DES — Current Diamond versus Recessed diamond

## Evidence and intended difference

The delivered SCAD defines `F_g=clamp((0.5-q)/(0.5-g),0,1)`, where
`q=max(abs(wrap(u+v)),abs(wrap(u-v)))` and `wrap(t)=t-floor(t+0.5)`.
At g0.18, its radius is `R-d+d*F_g`: cell centers are broad crowns at R,
crossings are valleys at R-d. This is blunt relief despite staying inside OD.
Historical R4 explicitly calls recessed diamonds negative smoothstep pockets
with non-recessed crossing ridges; its g0.14 is a documented design choice.
Do not replace this with a signless diamond outline or a color-only variant.

## Exact analytic comparison

Use fixed reference R19.5mm and a flat developed sidewall patch, not a fabricated
whole-container mesh. Size P4.8..8mm (slider0.1), Depth d0.10..0.60mm (slider0.05),
defaults4.8/0.45; one shared pair of controls keeps comparisons fair.
Allow finite off-grid exact values; reject blanks/nonfinite/out-of-range without
coercion. Preserve raw text. Render button updates the study only when valid;
edits mark the displayed study stale and disable no unrelated main-app controls.
Reset restores the two defaults. No source/worker/job identity modification.

Target arc `a=P==4.8?3.63:P*(3.63/4.8)`; count
`N=floor(2*pi*(R-d)/a+0.5)`; actual arc `A=2*pi*(R-d)/N`.
Developed coordinates x=A*u, y=P*v; choose global phase zero for both patches.
Current displacement from outside surface: `hCurrent=-d+d*F_0.18(u,v)`.
Proposal: `hRecess=-d*S(F_0.14(u,v))`, `S(t)=t*t*(3-2*t)`.
Both occupy [-d,0]. At u=v=0: Current0, Recess−d; at u0.5/v0:
Current−d, Recess0. These are the central falsifiable witnesses.
The cubic smoothstep is from R4; later R9's quintic variant is historical,
not authority to silently change the proposed pocket profile.

## View and sampling contract

Self-contained static HTML/CSS/ES modules in `preview/recessed-diamond-study/`;
use native Canvas/SVG, no new packages or Figma. Desktop shows two equal panels;
mobile stacks them without horizontal overflow. Controls remain together above
the panels with >=44px targets and explicit mm limits; use everyday labels.
Page title: “Diamond surface study”; panel labels “Current Diamond” and
“Recessed diamond proposal”. Always-visible note: “Appearance study, not a
compiled container.” Link back to the accepted customizer, not a fake STL action.

Show four-by-four cells in each top-view shaded height-field patch with exactly
the same dimensions, neutral gray material, lighting, and numeric scale bars.
Evaluate the analytic field at pixel centers; use at least256 and at most512
samples per axis per panel, with no interpolated/fallback motif generation.
Compute slopes by symmetric differences with delta1e-4 in u/v and divide by
A/P respectively. Form normal `normalize(-dh/dx,-dh/dy,1)`, shared light
`normalize(-0.6,-0.8,1)`, intensity `0.35+0.65*max(0,dot(n,L))`.
At nondifferentiable creases this is a symmetric display derivative, not a
manufacturing normal or facet-quality claim. Do not color-code families.

Under each patch show the same v0 section over u[-1,1], outside datum h0,
and depth labels. First section uses equal x/depth units (“True proportions;
screen size depends on zoom”); second repeats it at radial depth×6, labelled
“Depth enlarged ×6” directly on the view. Sample at least512 points and include
all u breakpoints for both g values, crossings and centers exactly. A5mm scale
bar denotes model units, not calibrated physical millimetres on the display.
Top-view shading communicates relief; the sections establish its actual sign.
Keep both comparisons visible in the document, not behind unrelated disclosures.

## Small evidence and user gate

Independent tests bind current-field samples to frozen SCAD algebra, check the
four center/crossing values, bounded range, periodicity, same phase, unchanged
pitch as the patch viewport changes, Size/Depth sensitivity and invalid recovery.
Check displayed surface and section use the same accepted parameter snapshot;
no-caption browser review must distinguish crown centers from pocket centers.
At1280×900 and390×844 inspect labels, signs, scale, lighting, controls and no
overflow; record actual draw time without a claimed phone-speed guarantee.
The bounded 2×512² field samples need no persistent animation or heavy compiler.

User observation: “The current pattern has flat raised centers. The proposal
has sunken centers with crossing ridges. Is that the recessed pattern you want?”
PASS selects this appearance only. If rejected or inconsistent with the intended
object, request one close oblique photo of the intended diamond surface with
side lighting, identifying whether centers are raised or sunken. No photo blocks
the first documented proposal. Do not proceed to knit or another family yet.
Future CAD needs its own implementation contract: shared seam/pitch, inward OD,
wall>=3.95+d plus justified sampling allowance, end clipping, <=250000 exterior
faces, <=0.025mm field error and actual source/mesh/performance checks. Existing
Diamond crown-width guards cannot automatically stand for recessed-pocket webs.
