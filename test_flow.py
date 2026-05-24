# test_flow.py
import json
from workflows.order_processor import run_order_flow

def test():
    # Load user data
    with open('data/user_info.json', 'r') as f:
        user_data = json.load(f)
    
    query = "shirt"
    print(f"--- Starting Order Flow for: {query} ---")
    
    url = run_order_flow(query, user_data)
    
    if isinstance(url, str) and url.startswith("http"):
        print(f"\nSUCCESS! Payment URL generated:")
        print(url)
    else:
        print(f"\nFLOW FAILED: {url}")

if __name__ == "__main__":
    test()