from ..engine import run_command
from collections import defaultdict

def lookup_multiple_businesses(items):
    """
    Groups items by business and performs lookups for each store.
    
    :param items: List of dicts: [{"business": "...", "variant_id": "..."}]
    """
    # 1. Group IDs by business domain
    grouped = defaultdict(list)
    for item in items:
        grouped[item['business']].append(item['variant_id'])
    
    results = []
    
    # 2. Run one command per business
    for business, vids in grouped.items():
        command = ['catalog', 'lookup', '--business', business]
        for index, vid in enumerate(vids):
            command.extend(['--set', f'/ids/{index}={vid}'])
        
        # Execute and store result
        results.append({
            "business": business,
            "data": run_command(command)
        })
            
    return results