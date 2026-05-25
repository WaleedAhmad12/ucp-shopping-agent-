export default function ProductCard({ product, onAddToCart }) {
  const variant = product?.variants?.[0] || {};
  const imageUrl = variant?.media?.[0]?.url || product?.media?.[0]?.url || 'https://placehold.co/600x400?text=No+Image';
  const productPageUrl = product?.url || variant?.url || product?.product_url || product?.page_url || product?.links?.product || null;
  const priceText = typeof variant?.price?.amount === 'number'
    ? `$${(variant.price.amount / 100).toFixed(2)}`
    : 'Price unavailable';
  
  return (
    <div className="border border-gray-200 p-4 rounded-xl shadow-sm bg-white flex flex-col h-[350px]">
      {/* Forced fixed height container */}
      <div className="relative w-full h-[180px] overflow-hidden rounded-lg mb-3">
        <img 
          src={imageUrl} 
          alt={product?.title || 'Product image'} 
          className="absolute inset-0 w-full h-full object-contain bg-gray-50" 
        />
      </div>
      
      {/* Content wrapper */}
      <div className="flex-grow flex flex-col justify-between">
        <h3 className="font-bold text-sm text-gray-800 line-clamp-2">
          {product?.title || 'Untitled product'}
        </h3>
        <p className="text-blue-600 font-semibold text-lg">
          {priceText}
        </p>
      </div>

      <div className="mt-4 space-y-2">
        <button
          type="button"
          onClick={() => {
            if (productPageUrl) {
              window.open(productPageUrl, '_blank', 'noopener,noreferrer');
            }
          }}
          disabled={!productPageUrl}
          className={`w-full text-center py-2 rounded-lg font-medium transition cursor-pointer active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 ${
            productPageUrl
              ? 'bg-white border border-gray-300 text-gray-900 hover:bg-gray-50'
              : 'bg-gray-100 border border-gray-200 text-gray-400 cursor-not-allowed active:scale-100'
          }`}
        >
          Go to Product Page
        </button>

        <button 
          onClick={() => onAddToCart?.(product)}
          className="w-full bg-slate-900 text-white py-2 rounded-lg font-medium hover:bg-slate-800 transition cursor-pointer active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}