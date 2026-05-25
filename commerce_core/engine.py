import subprocess
import json
from .config import get_ucp_cmd


def run_command(command, business=None, payload=None, profile='my-agent'):
    ucp_cmd = get_ucp_cmd()
    full_cmd = [ucp_cmd] + command
    if business: full_cmd += ['--business', business]
    full_cmd += ['--profile', profile, '--format', 'json']
    if payload: full_cmd.extend(['--input', json.dumps(payload, separators=(',', ':'))])
    result = subprocess.run(full_cmd, capture_output=True, text=True, encoding='utf-8')
    return json.loads(result.stdout) if result.returncode == 0 else {'error': result.stderr}
