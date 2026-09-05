# R8 parse recovery intake

R7 candidate failed before canvas creation in Chromium 151: `PAGEERROR missing ) after argument list`. Root isolated the parse fault to `preview/p2-r6-text-label-system/app.js` line 8, `endInset` dome return: parentheses count is 17 opens versus 16 closes. Whole-file `node --check` misleadingly passed. The only permitted recovery is one structural closing parenthesis in that return. R7 candidate/evidence are historical; no behavior, source scope, service, route, CAD/OpenSCAD, or continuity change is authorized.
