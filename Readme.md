(# Shop Automation Framework)

A small end-to-end shopping automation example that demonstrates a Python FastAPI backend wired to a Node/Vite React frontend. The backend shells out to a local `ucp` CLI to interact with store catalogs, carts and checkouts; the frontend provides a simple shopping UI.

**Quick Summary**
- **Backend:** FastAPI app — [api/main.py](api/main.py)
- **Core logic:** commerce helpers — [commerce_core](commerce_core)
- **Frontend:** Vite + React — [frontend/package.json](frontend/package.json)

# Requirements and Steps

## Open Terminal and Install:

Node.js 18 or higher.

```cmd
npm install -g @shopify/ucp-cli
```
# Open Command Palette > Chat: Install Plugin From Source
Copy and Paste --> https://github.com/Shopify/shopify-ai-toolkit

# In terminal run this:

```cmd
ucp profile init --name my-agent
```
```cmd
cd "C:\Users\Waleed\.ucp\profiles"
```
```cmd
ls
```

# Result:
Mode                 LastWriteTime         Length Name        
----                 -------------         ------ ----        
d-----         5/25/2026  12:04 PM                agent       
d-----         5/21/2026   7:52 PM                my-agent 


```cmd
cd my-agent
ls
```

# Result:
Mode                 LastWriteTime         Length Name        
----                 -------------         ------ ----        
-a----         5/21/2026   7:41 PM            170 meta.json   
-a----         5/21/2026   7:41 PM           3262 profile.json


# Run this cmd to create a config file :
```cmd
New-Item -Path "config.json" -ItemType "File"
```
# Result:
```cmd
Mode                 LastWriteTime         Length Name        
----                 -------------         ------ ----        
-a----         5/21/2026   7:52 PM             96 config.json 
-a----         5/21/2026   7:41 PM            170 meta.json   
-a----         5/21/2026   7:41 PM           3262 profile.json
```

# Run this cmd a notepad file will open (config.json)
```cmd
notepad C:\Users\Waleed\.ucp\profiles\my-agent\config.json
```

# Paste this in the file :
```cmd
{"profile_url": "https://waleedahmad12.github.io/ucp-agent-profile/ucp-agent-profile.json"}
```
## Save and close the file

# Path

# Run this cmd you will get path:
```cmd 
where.exe ucp  
```

# Example:
C:\Users\Waleed\AppData\Roaming\npm\ucp.cmd 


## Copy this to .env and update values for your environment
## Full path to the ucp executable (Windows example)

UCP_CMD=use the path obtained using where.exe ucp





# Create a virtual environment

```cmd
python -m venv .venv
```
# Activate it 
```cmd
.venv\Scripts\activate.bat
```

# Install the requirements

```cmd
pip install -r requirements.txt
```

**Run (development)**
- Start backend (from repo root):

	D:/work/shop-automation-framework/
    ```cmd
    uvicorn api.main:app
    ```

    Open the backend in your browser (usually http://localhost:8000/docs) FastAPi docs

- Start frontend dev server (from `frontend`):

    ```cmd
	npm run dev
    ```

Open the frontend in your browser (Vite will show the URL, usually http://localhost:5173). The frontend calls the backend at http://127.0.0.1:8000 by default.

**API Endpoints (selected)**
- **GET** /api/search?query=<term>&limit=<n>: Search catalog and return normalized results as {"result": {"products": [...]}} — implemented in [api/main.py](api/main.py).
- **POST** /api/get_product: get product detail (body: product_id, business)
- **POST** /api/add_to_cart: add an item to an in-memory cart (body: product, quantity)
- **POST** /api/checkout: create checkout URLs per seller domain using the `ucp` flow
- **POST** /api/lookup_batch: batch lookup helper (uses `commerce_core/catalog/lookup_catalog`)
