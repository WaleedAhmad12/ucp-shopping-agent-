from .engine import run_command

def get_checkout_schema(business, op='update'):
    res = run_command(['checkout', op, '--business', business, '--input-schema'])
    return res.get('result', {}).get('tool', {}).get('inputSchema', {}).get('properties', {})

def update_checkout(live_id, business, payload):
    return run_command(['checkout', 'update', live_id], business=business, payload=payload)
