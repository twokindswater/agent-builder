import React from 'react';
import { Button, Box } from '@mui/material';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const QuickAccessButtons = () => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: 'flex', gap: 2 }}>
      <Button
        variant="contained"
        startIcon={<Add />}
        onClick={() => navigate('/studio/new')}
      >
        새 워크플로우 만들기
      </Button>
      <Button
        variant="outlined"
        startIcon={<Add />}
        onClick={() => navigate('/agents/new')}
      >
        새 Agent 만들기
      </Button>
    </Box>
  );
};

export default QuickAccessButtons; 