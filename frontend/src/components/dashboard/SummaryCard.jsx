import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const SummaryCard = ({ title, value, icon: Icon }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {Icon && <Icon sx={{ mr: 1, color: 'primary.main' }} />}
          <Typography variant="h6" component="div">
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div">
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default SummaryCard; 