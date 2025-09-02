
#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib
import platform

def run_command(cmd, shell=False):
    if isinstance(cmd, str) and not shell:
        cmd = cmd.split()
    
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, shell=shell)
    
    if result.returncode != 0:
        sys.exit(result.returncode)
    
    return result

def main():
    os.environ['DD_ORIGIN_DETECTION_ENABLED'] = 'false'
    base_cmd = [
        'pytest', '-v', 'tests/unit', '--ignore=tests/unit/dogstatsd/test_container.py'
    ]

    # Build the exclusion filter
    exclusions = ['not test_timed_coroutine']

    # On Linux, exclude the IPv6 test that fails in containers
    if platform.system() == 'Linux':
        exclusions.append('not test_dedicated_udp6_telemetry_dest')
    # On Windows, exclude the tests related to sockets
    if sys.version_info < (3, 13) and os.name == 'nt':
        base_cmd.extend(['--ignore=tests/unit/dogstatsd/test_statsd.py'])
    else:
        base_cmd.extend(['-k', ' and '.join(exclusions)])
    run_command(base_cmd)

if __name__ == "__main__":
    main()