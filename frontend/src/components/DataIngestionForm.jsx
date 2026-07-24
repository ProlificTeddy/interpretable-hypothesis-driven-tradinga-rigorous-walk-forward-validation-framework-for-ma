import React, { useState } from 'react';
import { Box, Button, TextField, Typography, Snackbar, CircularProgress } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { styled } from '@mui/system';
import axios from 'axios';

const GradientCard = styled(Box)(({ theme }) => ({
  background: 'linear-gradient(45deg, #1a237e 30%, #0d47a1 90%)',
  borderRadius: '16px',
  padding': theme.spacing(4),
  boxShadow: '0 8px 32px rgba(0,0,0,0.28)',
  transition: 'transform 0.3s ease',
  '&:hover': {
    transform: 'translateY(-4px)'
  }
}));

const SymbolInput = styled(TextField)({
  '& .MuiOutlinedInput-root': {
    color: '#e0e0e0',
    '& fieldset': { borderColor: '#448aff' },
    '&:hover fieldset': { borderColor: '#82b1ff' },
    '&.Mui-focused fieldset': { borderColor: '#2979ff' }
  }
});

export default function DataIngestionForm() {
  const [symbols, setSymbols] = useState('');
  const [startDate, setStartDate] = useState(new Date('2015-01-01'));
  const [endDate, setEndDate] = useState(new Date('2024-01-01'));
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleIngest = async () => {
    if (!symbols.trim()) {
      setSnackbar({ open: true, message: 'Please enter at least one symbol', severity: 'error' });
      return;
    }

    setLoading(true);
    try {
      await axios.post('/api/data/ingest', {
        symbols: symbols.split(',').map(s => s.trim().toUpperCase())
      });
      setSnackbar({ open: true, message: 'Data ingestion started successfully', severity: 'success' });
    } catch (error) {
      setSnackbar({ open: true, message: 'Failed to start ingestion: ' + error.message, severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <GradientCard>
      <Typography variant="h5" gutterBottom sx={{ color: '#e0e0e0', mb: 3 }}>
        Historical Data Ingestion
      </Typography>
      
      <SymbolInput
        fullWidth
        label="Stock Symbols (comma-separated)"
        value={symbols}
        onChange={(e) => setSymbols(e.target.value)}
        sx={{ mb: 3 }}
      />

      <Box sx={{ display: 'flex', gap: 3, mb: 3 }}>
        <DatePicker
          label="Start Date"
          value={startDate}
          onChange={(date) => setStartDate(date)}
          sx={{ flex: 1 }}
        />
        <DatePicker
          label="End Date"
          value={endDate}
          onChange={(date) => setEndDate(date)}
          sx={{ flex: 1 }}
        />
      </Box>

      <Button
        variant="contained"
        onClick={handleIngest}
        disabled={loading}
        sx={{
          background: 'linear-gradient(45deg, #00c853 30%, #00e676 90%)',
          '&:hover': { background: 'linear-gradient(45deg, #009624 30%, #00c853 90%)' }
        }}
      >
        {loading ? <CircularProgress size={24} sx={{ color: 'white' }} /> : 'Start Data Ingestion'}
      </Button>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
        message={snackbar.message}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      />
    </GradientCard>
  );
}