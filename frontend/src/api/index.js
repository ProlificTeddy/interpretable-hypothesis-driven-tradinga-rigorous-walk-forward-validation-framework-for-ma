import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

export const useHypothesis = (hypothesisId) => {
  const [hypothesis, setHypothesis] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(`/api/hypotheses/${hypothesisId}`);
        setHypothesis(response.data);
      } catch (error) {
        console.error('Error fetching hypothesis:', error);
      } finally {
        setLoading(false);
      }
    };

    if (hypothesisId) fetchData();
  }, [hypothesisId]);

  return { hypothesis, loading };
};

export const useValidationStatistics = (hypothesisId) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(`/api/reports/validation-statistics/${hypothesisId}`);
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching validation stats:', error);
      } finally {
        setLoading(false);
      }
    };

    if (hypothesisId) fetchData();
  }, [hypothesisId]);

  return { stats, loading };
};