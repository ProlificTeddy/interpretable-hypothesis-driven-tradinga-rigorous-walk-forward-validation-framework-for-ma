import React, { useState } from 'react';
import { Box, Button, Typography, LinearProgress, Chip, Stack, Divider } from '@mui/material';
import { styled } from '@mui/system';
import axios from 'axios';
import { VictoryChart, VictoryLine, VictoryTheme } from 'victory';

const AnimatedCard = styled(Box)(({ theme }) => ({
  background: 'linear-gradient(195deg, #0D324D 0%, #7F5A83 100%)',
  borderRadius: '24px',
  padding: theme.spacing(4),
  boxShadow: '0 16px 48px rgba(0,0,0,0.3)',
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    transform: 'translateY(-6px)',
    boxShadow: '0 24px 64px rgba(0,0,0,0.4)'
  }
}));

const RLTrainingPanel = ({ hypothesisId }) => {
  const [trainingState, setTrainingState] = useState('idle');
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);

  const startTraining = async () => {
    setTrainingState('training');
    try {
      const { data } = await axios.post(`/api/rl-optimizer/train`, {
        hypothesis_id: hypothesisId
      });
      
      const pollResults = async () => {
        const { data: res } = await axios.get(`/api/rl-optimizer/results/${data.training_id}`);
        if (res.status === 'completed') {
          setTrainingState('completed');
          setResults(res);
        } else {
          setProgress(Math.min(100, progress + 10));
          setTimeout(pollResults, 2000);
        }
      };
      
      pollResults();
    } catch (error) {
      setTrainingState('error');
    }
  };

  return (
    <AnimatedCard>
      <Typography variant="h5" gutterBottom sx={{ color: 'white', mb: 3 }}>
        Strategy Optimization
      </Typography>
      
      {trainingState === 'idle' && (
        <Button
          variant="contained"
          size="large"
          onClick={startTraining}
          sx={{
            background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)',
            fontWeight: 'bold'
          }}
        >
          Start RL Optimization
        </Button>
      )}

      {trainingState === 'training' && (
        <Box>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{ height: 10, borderRadius: 5, mb: 2 }}
          />
          <Typography variant="body2" sx={{ color: 'white', textAlign: 'center' }}>
            Training in progress...
          </Typography>
        </Box>
      )}

      {trainingState === 'completed' && results && (
        <Stack spacing={3}>
          <Divider sx={{ borderColor: 'rgba(255,255,255,0.2)' }} />
          
          <Box>
            <Typography variant="h6" sx={{ color: 'white' }}>Optimized Parameters</Typography>
            <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
              {Object.entries(results.optimized_parameters).map(([key, value]) => (
                <Chip
                  key={key}
                  label={`${key}: ${value.toFixed(2)}`}
                  sx={{ background: 'rgba(255,255,255,0.15)', color: 'white' }}
                />
              ))}
            </Stack>
          </Box>

          <Box>
            <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>Training Progress</Typography>
            <VictoryChart theme={VictoryTheme.material}>
              <VictoryLine
                data={results.training_metrics.episode_rewards.map((r, i) => ({ x: i, y: r }))}
                style={{ data: { stroke: '#4CAF50' } }}
              />
            </VictoryChart>
          </Box>
        </Stack>
      )}
    </AnimatedCard>
  );
};

export default RLTrainingPanel;