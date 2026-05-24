# api/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from commerce_core import search_products
from workflows.order_processor import run_order_flow,run_order_flow_multi
import json

app = FastAPI()

# Middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize shared cart state
@app.on_event("startup")
async def startup_event():
    app.state.cart = []

# --- ENDPOINTS ---

@app.get("/api/search")
async def search(query: str):
    raw_data = search_products(query)
    
    # Check if 'result' exists, otherwise look for 'products' directly
    if isinstance(raw_data, dict):
        if 'result' in raw_data and 'products' in raw_data['result']:
            return {"result": raw_data['result']}
        elif 'products' in raw_data:
            return {"result": {"products": raw_data['products']}}
        else:
            # Fallback: scan keys for a list of products
            for key, value in raw_data.items():
                if isinstance(value, list) and len(value) > 0 and 'variants' in value[0]:
                    return {"result": {"products": value}}
                    
    return raw_data

@app.get("/api/cart")
async def get_cart():
    return {"cart": app.state.cart}

class CartItem(BaseModel):
    product: dict
    quantity: int

@app.post("/api/add_to_cart")
async def add_to_cart(item: CartItem):
    app.state.cart.append(item.dict())
    return {"message": "Item added", "cart": app.state.cart}

from collections import defaultdict

@app.post("/api/checkout")
async def checkout(request: Request):
    with open('data/user_info.json', 'r') as f:
        user_data = json.load(f)
    
    # 1. Group items by business domain
    cart_by_business = defaultdict(list)
    for item in app.state.cart:
        domain = item['product']['variants'][0]['seller']['domain']
        variant_id = item['product']['variants'][0]['id']
        cart_by_business[domain].append(variant_id)
    
    # 2. Process checkouts for each business
    results = {}
    for domain, variant_ids in cart_by_business.items():
        # You need to ensure run_order_flow_multi can handle this
        url = run_order_flow_multi(domain, variant_ids, user_data)
        results[domain] = url
        
    return {"urls": results}