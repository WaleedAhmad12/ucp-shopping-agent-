from ..engine import run_command

def get_product(product_id: str, business_domain: str, selections=None):
    command = ['catalog', 'get_product', product_id, '--business', business_domain]
    
    # ADD THIS PRINT STATEMENT
    print(f"DEBUG: Executing command: {' '.join(command)}")
    
    if selections:
        for key, value in selections.items():
            command.extend(['--set', f"{key}={value}"])
            
    return run_command(command)