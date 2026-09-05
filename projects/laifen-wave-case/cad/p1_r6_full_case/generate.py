"""Generate four explicit primary targets with owned-process time limits."""
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
from time import monotonic

TARGET_SECONDS=600
TOTAL_SECONDS=1800
TARGETS=('body','cap_c25','closed_c25','print_layout')
CAD_GEN=Path('/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen')


def main():
    folder=Path(__file__).absolute().parent;root=folder.parents[3]
    if Path.cwd()!=root or Path(sys.executable).parent!=root/'.venv/bin':
        raise SystemExit('Run from repository root through its uv environment')
    if sys.version_info[:2]!=(3,12):
        raise SystemExit('Python3.12 is required')
    start=monotonic();env=dict(os.environ);env['CADGEN_WARM']='0'
    for name in TARGETS:
        allowance=min(TARGET_SECONDS,TOTAL_SECONDS-(monotonic()-start))
        if allowance<=0:raise TimeoutError('four-target generation exceeded1800s')
        target=folder/(name+'.step.py');begin=monotonic()
        cmd=[sys.executable,str(CAD_GEN),str(target.relative_to(root)),'--write']
        print(json.dumps({'stage':'target_start','target':name,'timeout_seconds':allowance,
                          'command':cmd}),flush=True)
        process=subprocess.Popen(cmd,cwd=root,env=env,start_new_session=True)
        try:
            code=process.wait(timeout=allowance)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL);process.wait()
            raise TimeoutError(f'{name} exceeded{allowance:.3f}s; owned process group stopped')
        if code:raise RuntimeError(f'{name} generation failed with exit{code}')
        artifact=folder/(name+'.step')
        if not artifact.is_file() or artifact.stat().st_size==0:
            raise RuntimeError(f'{name} STEP missing or empty')
        print(json.dumps({'stage':'target_export_complete','target':name,
                          'seconds':monotonic()-begin,'total_seconds':monotonic()-start,
                          'step_bytes':artifact.stat().st_size}),flush=True)


if __name__=='__main__':main()
