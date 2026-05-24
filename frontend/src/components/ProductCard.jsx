export default function ProductCard({ product, onAddToCart }) {
  const variant = product.variants[0];
  
  return (
    <div className="border border-gray-200 p-4 rounded-xl shadow-sm bg-white flex flex-col h-[350px]">
      {/* Forced fixed height container */}
      <div className="relative w-full h-[180px] overflow-hidden rounded-lg mb-3">
        <img 
          src={variant.media[0].url} 
          alt={product.title} 
          className="absolute inset-0 w-full h-full object-contain bg-gray-50" 
        />
      </div>
      
      {/* Content wrapper */}
      <div className="flex-grow flex flex-col justify-between">
        <h3 className="font-bold text-sm text-gray-800 line-clamp-2">
          {product.title}
        </h3>
        <p className="text-blue-600 font-semibold text-lg">
          ${(variant.price.amount / 100).toFixed(2)}
        </p>
      </div>

      <button 
        onClick={() => onAddToCart(product)}
        className="mt-4 w-full bg-slate-900 text-white py-2 rounded-lg font-medium hover:bg-slate-800 transition"
      >
        Add to Cart
      </button>
    </div>
  );
}