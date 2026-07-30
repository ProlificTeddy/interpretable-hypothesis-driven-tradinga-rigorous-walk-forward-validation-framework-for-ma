import { usePerformanceMetrics } from '../api';

export function PerformanceMetrics({ hypothesisId }) {
  const { metrics, loading } = usePerformanceMetrics(hypothesisId);

  const equityData = {
    labels: metrics?.equityCurve?.map((_, i) => `Period ${i + 1}`),
    datasets: [{
      label: 'Equity Curve',
      data: metrics?.equityCurve || [],
      borderColor: '#22d3ee',
      tension: 0.4,
      pointRadius: 0
    }]
  };

  const riskData = {
    labels: ['Sharpe Ratio', 'Sortino Ratio', 'Max Drawdown'],
    datasets: [{
      label: 'In-Sample',
      data: [metrics?.inSampleSharpe, metrics?.inSampleSortino, metrics?.inSampleDrawdown],
      backgroundColor: '#3b82f6'
    }, {
      label: 'Out-of-Sample',
      data: [metrics?.outSampleSharpe, metrics?.outSampleSortino, metrics?.outSampleDrawdown],
      backgroundColor: '#22d3ee'
    }]
  };

  return (
    <div className="bg-gray-800 rounded-2xl p-6 shadow-xl">
      <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
        Performance Metrics
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Equity Curve</h3>
          <div className="h-64">
            <Line
              data={equityData}
              options={{
                maintainAspectRatio: false,
                scales: { y: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                          x: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } } },
                plugins: { legend: { labels: { color: '#9CA3AF' } } }
              }}
            />
          </div>
        </div>
        
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Risk Metrics</h3>
          <div className="h-64">
            <Bar
              data={riskData}
              options={{
                maintainAspectRatio: false,
                scales: { y: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                          x: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } } },
                plugins: { legend: { labels: { color: '#9CA3AF' } } }
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}