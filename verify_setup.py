# verify_setup.py
from commerce_core import search_products

def verify():
    print("--- Verifying commerce_core Library ---")
    query = "shirt" # Change to a test term relevant to your store
    print(f"Searching for: {query}...")
    
    try:
        results = search_products(query)
        if "error" in results:
            print(f"FAILED: {results['error']}")
        elif results and 'result' in results:
            products = results['result'].get('products', [])
            print(f"SUCCESS! Found {len(products)} products.")
            if products:
                print(f"First product: {products[0].get('title')}")
        else:
            print("Received empty or unexpected response from UCP CLI.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    verify()