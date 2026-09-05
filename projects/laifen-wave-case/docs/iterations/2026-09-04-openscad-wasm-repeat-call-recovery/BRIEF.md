# OSW-12 repeat-call recovery brief

OSW-11 proved the runtime-init repair (`noInitialRun:true`) and a first `callMain` cube, but the second body call aborts because the cached Emscripten module has exited. The same evidence records `Ignoring request to enable unknown feature 'manifold'`.

The smallest correct contract is a fresh factory instance for each CLI invocation: create one module for the cube probe and a new module for each body, cap, or assembled request. Preserve `--backend=Manifold` only if compiler diagnostics prove it is supported; remove only obsolete `--enable=manifold`. No UI, SCAD, dependency, route, CAD, or continuity change is in scope.
