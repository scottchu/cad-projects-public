# OSW-09 runtime-init recovery brief

OSW-08's frozen validation (`f4e58eb8...`) shows the browser WASM path fails during module initialization. The official openscad-wasm README example constructs `OpenSCAD({noInitialRun: true})`; the current worker factory (`6938e8....`) omits that option. Emscripten therefore auto-runs `main` with empty arguments, emits `Requested GUI mode`, aborts, and rejects the later explicit `callMain`.

The smallest recovery is one worker factory option: pass `noInitialRun: true` while preserving every existing module, argv, UI, source, route, and dependency byte. Re-run the real-WASM tiny-cube preflight and the existing body/case gates only after initialization succeeds.
