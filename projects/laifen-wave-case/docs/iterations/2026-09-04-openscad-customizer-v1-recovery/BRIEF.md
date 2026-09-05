# OSC-05 OpenSCAD Customizer V1 recovery brief

**Owner:** OSC-05 design  
**Status:** design-only recovery; no implementation

OSC-04 compiled smooth CSG but did not establish valid native OpenSCAD meshes. The recovery is limited to making the default `round`/`smooth` body, cap, and assembled outputs watertight and positive-volume, then making the default `diamond` body/cap compile and validate within a practical ceiling. Preserve the user-visible parameters, defaults, output selectors, and source path `openscad/laifen_case_customizer_v1.scad`.

The likely defect is the helical ridge profile's base edge being tangent to the cylindrical thread-root surface. The recovery design must specify a small explicit constructive overlap epsilon in the embedded male profile and the matching female tool, then prove that the epsilon does not change the intended pitch, engagement, clearance, or wall limits. It must also retain exact-OD round/smooth shells and the bounded diamond field.

No new feature family, parameter removal, source-path migration, mesh imitation, slicer, printer, or physical acceptance is in scope. One design revision is allowed before implementation.
