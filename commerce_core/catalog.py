from .engine import run_command

def search_products(query):
    return run_command(['catalog', 'search', '--set', f'/query={query}'])
