
#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib

def run_command(cmd, shell=False):
    if isinstance(cmd, str) and not shell:
        cmd = cmd.split()
    
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, shell=shell)
    
    if result.returncode != 0:
        sys.exit(result.returncode)
    
    return result

def main():

    base_cmd = ['pytest', '-v', 'tests/unit', '--ignore=tests/unit/dogstatsd/test_container.py']

    if sys.version_info < (3, 13) and os.name == 'nt':
        base_cmd.extend(['--ignore=tests/unit/dogstatsd/test_statsd.py'])
    else:
        base_cmd.extend(['-k', 'not test_timed_coroutine'])

    run_command(base_cmd)

if __name__ == "__main__":
    main()