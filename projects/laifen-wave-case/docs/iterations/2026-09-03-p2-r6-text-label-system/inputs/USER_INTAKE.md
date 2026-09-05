# Frozen intake — P2 R6 text label system

R6 supersedes R5 before implementation. Carry every R5 visual feature unchanged: closure modes, patterns/envelopes, end families, accessories, cross sections, phase matching, no core collar/thicker thread zone, and visual-only limits. R5 had no implementation files or candidate.

Add optional surface text: `textMode none|inset|outset`, `textString`, browser `fontFamily generic_sans|serif|mono|rounded`, `fontWeight regular|bold`, `textSize`, `textRelief`, orientation `horizontal|vertical`, target `lower|upper|both`, circumferential angle, target-local axial position, smooth patch toggle and patch margin. Preview fonts are visual-only; a future OpenSCAD boundary has an explicit-family string and must enumerate/fallback missing glyphs/fonts.

Text must avoid seam/end/thread/keepout/accessory regions; suppress texture under an enabled patch; report any text/accessory envelope beyond core OD. Escape all text and never inject HTML. Long/unsupported text invalidates and clears preview. The supplied `8CB1B86C-941F-49B8-963E-88D5791469E3/1-Pasted-Image-1.jpg` is visual evidence only; no model, text, geometry, font, or dimensions are copied.

`CA2463FF-392D-4436-B763-0588D8887E4E/1-Pasted-Image-1.jpg` is visual evidence only for accessory possibilities. Add `keyring_tab` and `bridge_handle` to carried accessory modes, in fixed or separate-print visual mode, with member thickness, keyring-hole diameter, bridge span, standoff, mount angle and attach half. Metal keyring/chain may appear only as clearly labelled reference hardware, never generated printable geometry. Integrate collision/keepout and total-envelope reporting; core OD stays distinct. No reference geometry is copied.
