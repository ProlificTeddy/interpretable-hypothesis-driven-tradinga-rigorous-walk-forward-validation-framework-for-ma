export function ValidationStatistics({ stats, loading }) {
  return (
    <div className="bg-gray-800 rounded-2xl p-6 shadow-xl">
      <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
        Walk-Forward Validation
      </h2>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b border-gray-700">
              <th className="pb-3">Window</th>
              <th className="pb-3">In-Sample Period</th>
              <th className="pb-3">Out-of-Sample Period</th>
              <th className="pb-3">Success Rate</th>
              <th className="pb-3">Profit Factor</th>
            </tr>
          </thead>
          <tbody>
            {stats?.walkForwards?.map((wf, i) => (
              <tr key={wf.id} className="border-b border-gray-700 hover:bg-gray-700/20 transition-colors">
                <td className="py-4">#{i + 1}</td>
                <td>
                  {new Date(wf.inSampleStart).toLocaleDateString()} - 
                  {new Date(wf.inSampleEnd).toLocaleDateString()}
                </td>
                <td>
                  {new Date(wf.outSampleStart).toLocaleDateString()} - 
                  {new Date(wf.outSampleEnd).toLocaleDateString()}
                </td>
                <td className="text-cyan-400 font-semibold">
                  {(wf.successRate * 100).toFixed(1)}%
                </td>
                <td className={wf.profitFactor > 1 ? 'text-green-400' : 'text-red-400'}>
                  {wf.profitFactor.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}