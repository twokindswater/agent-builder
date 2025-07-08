import React from 'react';
import { Grid, Box } from '@mui/material';
import { SmartToy, AccountTree, PlayArrow } from '@mui/icons-material';
import SummaryCard from '../components/dashboard/SummaryCard';
import RecentActivityList from '../components/dashboard/RecentActivityList';
import QuickAccessButtons from '../components/dashboard/QuickAccessButtons';

// 임시 데이터
const mockActivities = [
  { id: 1, name: '이미지 생성 워크플로우', status: 'success', timestamp: '2024-03-20T10:00:00' },
  { id: 2, name: '데이터 분석 워크플로우', status: 'failed', timestamp: '2024-03-20T09:30:00' },
  { id: 3, name: '텍스트 요약 워크플로우', status: 'running', timestamp: '2024-03-20T09:00:00' },
];

const Dashboard = () => {
  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <QuickAccessButtons />
      </Box>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <SummaryCard
            title="총 Agent 수"
            value="12"
            icon={SmartToy}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <SummaryCard
            title="총 워크플로우 수"
            value="25"
            icon={AccountTree}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <SummaryCard
            title="실행 중인 워크플로우"
            value="3"
            icon={PlayArrow}
          />
        </Grid>
      </Grid>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <RecentActivityList activities={mockActivities} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 