import React, { useState } from 'react';
import { Box, Button, TextField, Typography, Grid, Select, MenuItem, FormControl, InputLabel, CircularProgress } from '@mui/material';
import { styled } from '@mui/system';
import axios from 'axios';

const GradientCard = styled(Box)(({ theme }) => ({
  background: 'linear-gradient(45deg, #2c3e50 0%, #3498db 100%)',
  borderRadius: '24px',
  padding: theme.spacing(4),
  boxShadow: '0 12px 40px rgba(0,0,0,0.3)',
  transition: 'transform 0.3s ease, box-shadow 0.3s ease',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: '0 16px 48px rgba(0,0,0,0.4)'
  }
}));

const ParameterInput = styled(TextField)({
  '& .MuiOutlinedInput-root': {
    color: '#ecf0f1',
    '& fieldset': { borderColor: '#bdc3c7' },
    '&:hover fieldset': { borderColor: '#3498db' },
    '&.Mui-focused fieldset': { borderColor: '#2980b9' }
  }
});

export default function HypothesisForm() {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    parameters: { window_size: 20, multiplier: 2.5 }
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post('/api/hypotheses/', formData);
      // Reset form
      setFormData({ name: '', description: '', parameters: { window_size: 20, multiplier: 2.5 } });
    } catch (error) {
      console.error('Submission failed:', error);
    }
    setLoading(false);
  };

  return (
    <GradientCard>
      <Typography variant="h5" gutterBottom sx={{ color: '#ecf0f1', mb: 3 }}>
        New Market Hypothesis
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <ParameterInput
              fullWidth
              label="Hypothesis Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </Grid>
          <Grid item xs={12}>
            <ParameterInput
              fullWidth
              multiline
              rows={3}
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </Grid>
          <Grid item xs={6}>
            <ParameterInput
              type="number"
              label="Window Size"
              value={formData.parameters.window_size}
              onChange={(e) => setFormData({
                ...formData,
                parameters: { ...formData.parameters, window_size: e.target.value }
              })}
            />
          </Grid>
          <Grid item xs={6}>
            <ParameterInput
              type="number"
              label="0.1"
              step="0.1"
              label="Multiplier"
              value={formData.parameters.multiplier}
              onChange={(e) => setFormData({
                ...formData,
                parameters: { ...formData.parameters, multiplier: e.target.value }
              })}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
              sx={{
                background: 'linear-gradient(45deg, #27ae60 30%, #2ecc71 90%)',
                '&:hover': { transform: 'scale(1.02)' }
              }}
            >
              {loading ? <CircularProgress size={24} /> : 'Create Hypothesis'}
            </Button>
          </Grid>
        </Grid>
      </form>
    </GradientCard>
  );
}