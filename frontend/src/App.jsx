import { useState } from 'react';
import axios from 'axios';
import ProductCard from './components/ProductCard';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState('');
  const [limit, setLimit] = useState(10); // Added limit state
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [checkoutUrls, setCheckoutUrls] = useState({});
  const [loading, setLoading] = useState(false);

  const dollarsToCents = (value) => {
    if (value === '') {
      return null;
    }

    const parsed = Number(value);
    if (Number.isNaN(parsed)) {
      return null;
    }

    return Math.round(parsed * 100);
  };

  const handleSearch = async () => {
    try {
      const params = new URLSearchParams({
        query,
        limit: String(limit),
      });

      const minPriceCents = dollarsToCents(minPrice);
      const maxPriceCents = dollarsToCents(maxPrice);

      if (minPriceCents !== null) {
        params.set('min_price', String(minPriceCents));
      }

      if (maxPriceCents !== null) {
        params.set('max_price', String(maxPriceCents));
      }

      const res = await axios.get(`${API_BASE}/api/search?${params.toString()}`);
      const items = res.data.result?.products || res.data.products || [];
      setProducts(items);
    } catch (err) {
      console.error("Search failed", err);
    }
  };

  const addToCart = async (product) => {
    try {
      const res = await axios.post(`${API_BASE}/api/add_to_cart`, { product, quantity: 1 });
      setCart(res.data.cart);
      alert("Added to cart!");
    } catch (err) {
      console.error("Add to cart failed", err);
      alert("Failed to add to cart");
    }
  };

  const handleCheckout = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/checkout`);
      setCheckoutUrls(res.data.urls || {});
    } catch (err) {
      console.error("Checkout failed", err);
      alert("Checkout failed. Check server logs.");
    } finally {
      setLoading(false);
    }
  };

  const fetchProductDetails = async (productId, domain) => {
    try {
      const res = await axios.post(`${API_BASE}/api/get_product`, {
        product_id: productId,
        business: domain,
      });
      console.log(res.data.product);
    } catch (err) {
      console.error("Fetch product details failed", err);
    }
  };

  return (
    <div className="min-h-screen bg-[#16171d] p-4 md:p-8">
      {/* Header */}
      <div className="max-w-6xl mx-auto flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">Shopping Agent</h1>
        <button 
          onClick={() => setShowCart(!showCart)} 
          className="bg-slate-700 text-white px-6 py-2 rounded-lg font-semibold hover:bg-slate-600"
        >
          Cart ({cart.length})
        </button>
      </div>

      {/* Search Bar with Pagination Control */}
      <div className="max-w-6xl mx-auto flex flex-wrap gap-2 mb-8">
        <input 
          className="border border-gray-600 bg-gray-800 text-white p-3 flex-grow rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for products..."
        />
        
        <select 
          value={limit} 
          onChange={(e) => setLimit(Number(e.target.value))}
          className="bg-gray-800 text-white border border-gray-600 rounded-lg px-4"
        >
          <option value={10}>10 results</option>
          <option value={25}>25 results</option>
          <option value={50}>50 results</option>
        </select>

        <div className="flex items-center w-32 bg-gray-800 border border-gray-600 rounded-lg px-3">
          <span className="text-gray-400 mr-1">$</span>
          <input
            type="number"
            min="0"
            step="0.01"
            inputMode="decimal"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="0.5"
            className="w-full bg-transparent text-white outline-none"
          />
        </div>

        <div className="flex items-center w-32 bg-gray-800 border border-gray-600 rounded-lg px-3">
          <span className="text-gray-400 mr-1">$</span>
          <input
            type="number"
            min="0"
            step="0.01"
            inputMode="decimal"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="9999"
            className="w-full bg-transparent text-white outline-none"
          />
        </div>

        <button onClick={handleSearch} className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700">
          Search
        </button>
      </div>

      {/* Product Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.length > 0 ? (
          products.map((p, idx) => (
            <ProductCard key={p.id || idx} product={p} onAddToCart={addToCart} />
          ))
        ) : (
          <div className="col-span-full text-left text-gray-300 bg-white/5 border border-white/10 rounded-xl p-6">
            Search for a product to see results here.
          </div>
        )}
      </div>

      {loading && (
        <div className="max-w-6xl mx-auto mt-6 text-sm text-gray-300 text-left">
          Generating checkout links...
        </div>
      )}

      {showCart && (
        <>
          <div
            className="fixed inset-0 bg-black/40 z-40"
            onClick={() => setShowCart(false)}
          />

          <aside className="fixed inset-y-0 right-0 z-50 w-full md:w-96 bg-white shadow-2xl p-6 border-l overflow-y-auto text-left">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Your Cart</h2>
              <button
                onClick={() => setShowCart(false)}
                className="text-gray-500 hover:text-black font-bold"
              >
                Close
              </button>
            </div>

            <div className="space-y-4 mb-8">
              {cart.length > 0 ? (
                cart.map((item, index) => (
                  <div key={index} className="flex justify-between border-b pb-2">
                    <span className="text-sm font-medium text-gray-800">
                      {item.product?.title || 'Untitled product'}
                    </span>
                    <span className="text-sm text-gray-500">Qty {item.quantity}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500">Your cart is empty.</p>
              )}
            </div>

            <button
              onClick={handleCheckout}
              disabled={loading || cart.length === 0}
              className="w-full bg-green-600 text-white py-3 rounded-lg font-bold hover:bg-green-700 disabled:bg-gray-400"
            >
              {loading ? 'Generating Links...' : 'Checkout Now'}
            </button>

            {Object.keys(checkoutUrls).length > 0 && (
              <div className="mt-6 space-y-3">
                <h3 className="font-semibold text-gray-700">Your Checkout Links:</h3>
                {Object.entries(checkoutUrls).map(([domain, url]) => (
                  <a
                    key={domain}
                    href={url}
                    target="_blank"
                    rel="noreferrer"
                    className="block p-3 bg-blue-50 text-blue-700 rounded text-sm hover:bg-blue-100 truncate"
                  >
                    Complete order at {domain.split('.')[0]}
                  </a>
                ))}
              </div>
            )}
          </aside>
        </>
      )}
      
    </div>
  );
}

export default App;