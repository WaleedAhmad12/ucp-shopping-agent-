from ..engine import run_command
import json

def search_products(query: str, limit: int = 10, min_price: int | None = None, max_price: int | None = None):
    # Flattened command that matches your successful terminal test
    cmd = [
        'catalog', 'search', 
        '--set', f'/query="{query}"', 
        '--set', f'/pagination/limit={limit}', 
        '--set', '/context/address_country="US"',
        *(['--set', f'/filters/price/min={min_price}'] if min_price is not None else []),
        *(['--set', f'/filters/price/max={max_price}'] if max_price is not None else [])
    ]
    
    output = run_command(cmd)
    
    # If the CLI returns a string, parse it as JSON
    if isinstance(output, str):
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            # Handle cases where output might be a list or multiple objects
            return output
    return output