# OSW-05 WASM simulator recovery brief

OSC-04/OSW currently has a static browser simulator whose official OpenSCAD WASM engine is too slow on the default CGAL backend. Official WASM strings show CGAL as the old/slow default and Manifold as the new/fast optional backend; the worker currently passes only `--enable=manifold`.

The smallest recovery is worker argument correction plus a bounded smoke gate: invoke the real engine with `--enable=manifold --backend=Manifold`, compile a tiny cube before attempting case geometry, enforce a hard timeout, and retain compiler diagnostics. No geometry, UI, SCAD, route, or STEP changes are authorized.
