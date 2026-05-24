import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_first_product(query):
    """Dynamically finds the first product even if the JSON structure is nested."""
    response = requests.get(f"{BASE_URL}/api/search?query={query}").json()
    
    # 1. Try to find products list in common locations
    products = []
    if 'result' in response and 'products' in response['result']:
        products = response['result']['products']
    elif 'products' in response:
        products = response['products']
    else:
        # Fallback: Find the first list that looks like a product list
        for val in response.values():
            if isinstance(val, list) and len(val) > 0 and 'variants' in val[0]:
                products = val
                break
    
    if not products:
        print(f"DEBUG: No products found for '{query}'.")
        return None
        
    return products[0]

def test_multi_flow():
    print("--- Searching ---")
    shirt = get_first_product("shirt")
    jeans = get_first_product("jeans")
    
    if not shirt or not jeans:
        print("Test aborted: Could not find products.")
        return
        
    print(f"Found: {shirt.get('title')} and {jeans.get('title')}")
    
    # 2. Add to Cart
    print("--- Adding to cart ---")
    requests.post(f"{BASE_URL}/api/add_to_cart", json={"product": shirt, "quantity": 1})
    requests.post(f"{BASE_URL}/api/add_to_cart", json={"product": jeans, "quantity": 1})
    
    # 3. View Cart
    cart_res = requests.get(f"{BASE_URL}/api/cart").json()
    print(f"\n--- Current Cart Contents ---")
    for i, item in enumerate(cart_res.get('cart', [])):
        domain = item['product']['variants'][0]['seller']['domain']
        print(f"{i+1}. {item['product']['title']} (Seller: {domain})")
    
    # 4. Checkout
    print("\n--- Requesting Checkout ---")
    checkout_res = requests.post(f"{BASE_URL}/api/checkout").json()
    
    # Print the resulting URLs
    urls = checkout_res.get('urls', {})
    if urls:
        for domain, url in urls.items():
            print(f"Checkout URL for {domain}: {url}")
    else:
        print("Checkout failed or returned no URLs. Check Uvicorn logs.")

if __name__ == "__main__":
    test_multi_flow()