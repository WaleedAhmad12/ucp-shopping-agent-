import { useState } from 'react';
import axios from 'axios';
import ProductCard from './components/ProductCard';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [checkoutUrls, setCheckoutUrls] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/search?query=${query}`);
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
      alert("Failed to add to cart");
    }
  };

  const handleCheckout = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/checkout`);
      setCheckoutUrls(res.data.urls);
    } catch (err) {
      alert("Checkout failed. Check server logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#16171d] p-4 md:p-8">
      {/* Header */}
      <div className="max-w-6xl mx-auto flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Shopping Agent</h1>
        <button 
          onClick={() => setShowCart(!showCart)} 
          className="bg-slate-900 text-white px-6 py-2 rounded-lg font-semibold hover:bg-slate-800"
        >
          Cart ({cart.length})
        </button>
      </div>

      {/* Search Bar */}
      <div className="max-w-6xl mx-auto flex gap-2 mb-8">
        <input 
          className="border border-gray-300 p-3 flex-grow rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for products (e.g., shirt, jeans)..."
        />
        <button onClick={handleSearch} className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700">
          Search
        </button>
      </div>

      {/* Product Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.map((p, idx) => (
          <ProductCard key={idx} product={p} onAddToCart={addToCart} />
        ))}
      </div>

      {/* Cart Sidebar */}
      {showCart && (
        <div className="fixed inset-y-0 right-0 w-full md:w-96 bg-white shadow-2xl p-6 border-l z-50 overflow-y-auto">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Your Cart</h2>
            <button onClick={() => setShowCart(false)} className="text-gray-500 hover:text-black font-bold">Close</button>
          </div>
          
          <div className="space-y-4 mb-8">
            {cart.map((item, i) => (
              <div key={i} className="flex justify-between border-b pb-2">
                <span className="text-sm font-medium">{item.product.title}</span>
              </div>
            ))}
          </div>
          
          <button 
            onClick={handleCheckout} 
            disabled={loading || cart.length === 0}
            className="w-full bg-green-600 text-white py-3 rounded-lg font-bold hover:bg-green-700 disabled:bg-gray-400"
          >
            {loading ? "Generating Links..." : "Checkout Now"}
          </button>

          {Object.keys(checkoutUrls).length > 0 && (
            <div className="mt-6 space-y-3">
              <h3 className="font-semibold text-gray-700">Your Checkout Links:</h3>
              {Object.entries(checkoutUrls).map(([domain, url]) => (
                <a key={domain} href={url} target="_blank" rel="noreferrer" className="block p-3 bg-blue-50 text-blue-700 rounded text-sm hover:bg-blue-100 truncate">
                  Complete order at {domain.split('.')[0]}
                </a>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;