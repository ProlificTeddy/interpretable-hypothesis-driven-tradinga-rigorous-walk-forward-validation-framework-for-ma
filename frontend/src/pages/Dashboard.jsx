import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Line, Bar } from 'react-chartjs-2';
import { motion } from 'framer-motion';
import { HypothesisExplanation, PerformanceMetrics, ValidationStatistics } from '../components';
import { useHypothesis, useValidationStatistics } from '../api';

export default function Dashboard() {
  const { hypothesisId } = useParams();
  const { hypothesis, loading: hypLoading } = useHypothesis(hypothesisId);
  const { stats, loading: statsLoading } = useValidationStatistics(hypothesisId);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100 p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <HypothesisExplanation hypothesis={hypothesis} loading={hypLoading} />
          <PerformanceMetrics hypothesisId={hypothesisId} />
        </div>
        <ValidationStatistics stats={stats} loading={statsLoading} />
      </motion.div>
    </div>
  );
}