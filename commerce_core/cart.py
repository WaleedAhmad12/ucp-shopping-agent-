from .engine import run_command

def create_cart(business, variant_id):
    return run_command(['cart', 'create'], business=business, payload={'line_items': [{'item': {'id': variant_id}, 'quantity': 1}]})
