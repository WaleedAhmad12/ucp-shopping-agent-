# workflows/order_processor.py
from commerce_core import search_products, create_cart, get_checkout_schema, update_checkout
from commerce_core.engine import run_command

def clean_payload(data, schema):
    """Recursive filter for schema compliance."""
    cleaned = {}
    for k, v in data.items():
        if k in schema:
            if isinstance(v, dict):
                cleaned[k] = clean_payload(v, schema[k].get('properties', {}))
            elif isinstance(v, list):
                cleaned[k] = [clean_payload(i, schema[k].get('items', {}).get('properties', {})) 
                              if isinstance(i, dict) else i for i in v]
            else:
                cleaned[k] = v
    return cleaned

def run_order_flow(query, user_data):
    """Orchestrates the shopping process."""
    # 1. Search
    search_res = search_products(query)
    items = search_res.get('result', {}).get('products', [])
    if not items: return {"error": "Product not found"}
    
    target = items[0]
    variant_id = target['variants'][0]['id']
    business = target['variants'][0]['seller']['domain']
    
    # 2. Cart & Initial Checkout
    cart = create_cart(business, variant_id)
    cart_id = cart['result']['id']
    
    checkout = run_command(['checkout', 'create'], business=business, 
                          payload={"cart_id": cart_id, "line_items": []})
    live_id = checkout['result']['id']
    line_id = checkout['result']['line_items'][0]['id']
    
    # 3. Apply User Data (Schema-Aware)
    # We map user_data from your JSON to the structure required by the checkout
    raw_payload = {
        "line_items": [{"id": line_id, "item": {"id": variant_id}, "quantity": 1}],
        "buyer": {"email": user_data['email']},
        "fulfillment": {"methods": [{"line_item_ids": [line_id], "destinations": [user_data['shipping']]}]}
    }
    
    schema = get_checkout_schema(business)
    final_payload = clean_payload(raw_payload, schema)
    
    # 4. Finalize
    update_res = update_checkout(live_id, business, final_payload)
    return update_res['result'].get('continue_url')




# Add this function to workflows/order_processor.py
from commerce_core import create_cart, get_checkout_schema, update_checkout
from commerce_core.engine import run_command

def run_order_flow_multi(business, variant_ids, user_data):
    # 1. Create Cart with multiple items
    line_items = [{"item": {"id": vid}, "quantity": 1} for vid in variant_ids]
    cart = run_command(['cart', 'create'], business=business, payload={"line_items": line_items})
    cart_id = cart['result']['id']
    
    # 2. Create Checkout
    checkout = run_command(['checkout', 'create'], business=business, payload={"cart_id": cart_id, "line_items": []})
    live_id = checkout['result']['id']
    
    # 3. Apply User Data (Simplified for testing)
    raw_payload = {
        "line_items": [{"id": li['id'], "item": {"id": li['item']['id']}, "quantity": 1} 
                       for li in checkout['result']['line_items']],
        "buyer": {"email": user_data['email']},
        "fulfillment": {"methods": [{"line_item_ids": [li['id'] for li in checkout['result']['line_items']], 
                                    "destinations": [user_data['shipping']]}]}
    }
    
    schema = get_checkout_schema(business)
    # Import clean_payload from same file
    final_payload = clean_payload(raw_payload, schema) 
    
    update_res = update_checkout(live_id, business, final_payload)
    
    # DEBUG: Print the raw result if URL is missing
    if 'result' not in update_res or 'continue_url' not in update_res['result']:
        print(f"DEBUG ERROR for {business}: {update_res}")
        return None
        
    return update_res['result'].get('continue_url')