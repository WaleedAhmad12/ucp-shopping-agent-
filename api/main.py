from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from collections import defaultdict
import json

# Import your core logic
from commerce_core.catalog.catalog import search_products
from commerce_core.catalog.product_detail import get_product
from commerce_core.catalog.lookup_catalog import lookup_multiple_businesses
from workflows.order_processor import run_order_flow, run_order_flow_multi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    app.state.cart = []

# --- MODELS ---

class LookupRequest(BaseModel):
    variant_ids: List[str]
    business: str

class LookupItem(BaseModel):
    business: str
    variant_id: str

class BatchLookupRequest(BaseModel):
    items: List[LookupItem]

class CartItem(BaseModel):
    product: dict
    quantity: int

# --- ENDPOINTS ---
@app.get("/api/search")
async def search(query: str, limit: int = 10):
    raw_data = search_products(query, limit=limit)

    # If the CLI returned a dict, try to find the products list in common locations
    if isinstance(raw_data, dict):
        # Case: {'result': {'products': [...]}}
        if 'result' in raw_data and isinstance(raw_data['result'], dict) and 'products' in raw_data['result']:
            return {"result": raw_data['result']}

        # Case: {'products': [...]}
        if 'products' in raw_data and isinstance(raw_data['products'], list):
            return {"result": {"products": raw_data['products']}}

        # Fallback: scan values for a products-like list
        for key, value in raw_data.items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict) and 'variants' in value[0]:
                return {"result": {"products": value}}

    # If the CLI returned a flat list of products
    if isinstance(raw_data, list):
        return {"result": {"products": raw_data}}

    # Last resort: return raw data as-is
    return raw_data


@app.post("/api/get_product")
async def get_product_endpoint(data: dict):
    product_id = data.get("product_id")
    business = data.get("business")
    selections = data.get("selections")
    result = get_product(product_id, business, selections)
    return {"product": result}

@app.post("/api/lookup_batch")
async def lookup_batch_endpoint(request: BatchLookupRequest):
    # This calls the grouping function to avoid CLI async errors
    items_list = [item.dict() for item in request.items]
    return lookup_multiple_businesses(items_list)

@app.get("/api/cart")
async def get_cart():
    return {"cart": app.state.cart}

@app.post("/api/add_to_cart")
async def add_to_cart(item: CartItem):
    app.state.cart.append(item.dict())
    return {"message": "Item added", "cart": app.state.cart}

@app.post("/api/checkout")
async def checkout(request: Request):
    with open('data/user_info.json', 'r') as f:
        user_data = json.load(f)
    
    cart_by_business = defaultdict(list)
    for item in app.state.cart:
        # Safety check for nested keys
        domain = item['product']['variants'][0]['seller']['domain']
        variant_id = item['product']['variants'][0]['id']
        cart_by_business[domain].append(variant_id)
    
    results = {}
    for domain, variant_ids in cart_by_business.items():
        results[domain] = run_order_flow_multi(domain, variant_ids, user_data)
        
    return {"urls": results}