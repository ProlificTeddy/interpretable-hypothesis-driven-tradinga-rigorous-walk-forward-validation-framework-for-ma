export function HypothesisExplanation({ hypothesis, loading }) {
  return (
    <div className="col-span-1 lg:col-span-2 bg-gray-800 rounded-2xl p-6 shadow-xl">
      <h2 className="text-2xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
        Hypothesis Details
      </h2>
      
      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-700 rounded w-3/4" />
          <div className="h-4 bg-gray-700 rounded w-full" />
          <div className="h-4 bg-gray-700 rounded w-5/6" />
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold">{hypothesis?.name}</h3>
            <span className="text-sm text-cyan-400">
              Created: {new Date(hypothesis?.created_at).toLocaleDateString()}
            </span>
          </div>
          <p className="text-gray-300">{hypothesis?.description}</p>
          <div className="grid grid-cols-2 gap-4 mt-4">
            {Object.entries(hypothesis?.parameters || {}).map(([key, value]) => (
              <div key={key} className="bg-gray-700 p-3 rounded-lg">
                <div className="text-sm text-cyan-400">{key}</div>
                <div className="font-mono">{JSON.stringify(value)}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}