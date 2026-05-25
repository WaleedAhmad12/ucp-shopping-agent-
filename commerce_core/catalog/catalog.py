from ..engine import run_command
import json

def search_products(query: str, limit: int = 10):
    # Flattened command that matches your successful terminal test
    cmd = [
        'catalog', 'search', 
        '--set', f'/query="{query}"', 
        '--set', f'/pagination/limit={limit}', 
        '--set', '/context/address_country="US"'
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