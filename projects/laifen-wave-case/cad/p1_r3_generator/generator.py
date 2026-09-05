"""Generic parametric cylinder CLI: derive dimensions or regenerate STEP.

Example from repository root:
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --cavity-length 82.1 --dry-run
Written STEP topology is checked; fit and independent acceptance remain separate.
"""
import argparse
from dataclasses import asdict, fields
import json
import sys
from pathlib import Path
from hashlib import sha256
from time import monotonic
try:
    from .params import Params, derive, parameter_fingerprint, preset
    from .skin import tessellation_plan
except ImportError:
    sys.path.insert(0,str(Path(__file__).parent.parent))
    from params import Params, derive, parameter_fingerprint, preset
    from skin import tessellation_plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset",choices=("short-grip","generic","laifen-provisional"),default="short-grip")
    parser.add_argument("--dry-run",action="store_true",help="derive dimensions without building CAD (current default)")
    parser.add_argument("--write-step",action="store_true",help="regenerate actual BREP and write STEP files")
    parser.add_argument("--target",choices=("body","cap","coupons","closed","exploded","print-layout","all"),default="all")
    parser.add_argument("--output-dir",type=Path,default=Path(__file__).parent/"generated")
    for f in fields(Params):
        parser.add_argument("--"+f.name.replace("_","-"),type=str if f.name == "skin_style" else float)
    args = parser.parse_args(argv)
    try:
        p = preset(args.preset,**{f.name:getattr(args,f.name) for f in fields(Params) if getattr(args,f.name) is not None})
        d = derive(p)
        if args.write_step:
            if args.dry_run:raise ValueError("choose --dry-run or --write-step")
            from p1_r3_generator.parts import build_body,build_cap,build_coupon_set,build_assembly,print_layout
            from p1_r3_generator.surface import route_bounds
            from build123d import export_step,import_step
            route_bounds(p)
            result={}
            if args.target in ("coupons","all"):result.update(build_coupon_set(p))
            if args.target=="body":result["body"]=build_body(p)
            if args.target=="cap":result["cap"]=build_cap(p)
            if args.target in ("closed","all"):result["closed"]=build_assembly(p)
            if args.target in ("exploded","all"):result["exploded"]=build_assembly(p,1620,gap=derive(p).neck_height+2)
            if args.target in ("print-layout","all"):result["print_layout"]=print_layout(p)
            directory=args.output_dir/parameter_fingerprint(p)[:16]
            directory.mkdir(parents=True,exist_ok=True)
            artifacts={}
            for name,part in result.items():
                path=directory/(name+".step");start=monotonic();export_step(part,str(path))
                written=import_step(str(path))
                if not written.is_valid:raise ValueError(f"written STEP invalid: {path}")
                if len(written.solids())!=len(part.solids()):raise ValueError(f"written STEP count mismatch: {path}")
                if monotonic()-start>180:raise ValueError("STEP export/import stage exceeded180seconds")
                artifacts[name]={"path":str(path),"sha256":sha256(path.read_bytes()).hexdigest(),
                                 "solids":len(written.solids()),"written_valid":True}
            receipt={"status":"step_written_pending_independent_validation", "parameters":asdict(p),
                     "derived":asdict(d),"parameter_fingerprint":parameter_fingerprint(p),"artifacts":artifacts,
                     "source_sha256":{f.name:sha256(f.read_bytes()).hexdigest() for f in Path(__file__).parent.glob("*.py")},
                     "acceptance":{"cad":"pending independent checks","step":"topology checked; parity pending",
                                   "slicer":"pending","physical":"pending"}}
            (directory/"manifest.json").write_text(json.dumps(receipt,indent=2)+"\n")
            print(json.dumps(receipt,indent=2));return 0
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
