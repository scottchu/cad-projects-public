"""Generic parametric cylinder CLI, phase A: derive and dry-run only.

Example from repository root:
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --cavity-length 82.1 --dry-run
Full-body STEP builders await the R3 teaching gate and geometric validation.
"""
import argparse
from dataclasses import asdict, fields
import json
import sys
try:
    from .params import Params, derive, parameter_fingerprint, preset
    from .skin import tessellation_plan
except ImportError:
    from params import Params, derive, parameter_fingerprint, preset
    from skin import tessellation_plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset",choices=("short-grip","generic","laifen-provisional"),default="short-grip")
    parser.add_argument("--dry-run",action="store_true",help="derive dimensions without building CAD (current default)")
    parser.add_argument("--write-step",action="store_true",help="reserved full-CAD action; unavailable until the R3 teaching gate")
    for f in fields(Params):
        parser.add_argument("--"+f.name.replace("_","-"),type=str if f.name == "skin_style" else float)
    args = parser.parse_args(argv)
    try:
        p = preset(args.preset,**{f.name:getattr(args,f.name) for f in fields(Params) if getattr(args,f.name) is not None})
        d = derive(p)
        if args.write_step:
            raise ValueError("STEP generation pending R3 teaching gate; phase A supports --dry-run only")
        result = {"status":"derived_only", "preset":args.preset,
                  "parameter_fingerprint":parameter_fingerprint(p),
                  "parameters":asdict(p),"derived":asdict(d),
                  "tessellation_plan":{role:asdict(tessellation_plan(p,role)) for role in ("body","cap")},
                  "acceptance":{"analytic_constraints":"pass","cad":"pending",
                                "written_step":"pending","slicer":"pending","physical":"pending"}}
        print(json.dumps(result,indent=2,allow_nan=False))
        return 0
    except (ValueError,OverflowError) as exc:
        print(json.dumps({"status":"rejected","error":str(exc)}),file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
