import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  List, 
  ListItem, 
  ListItemText,
  Chip,
  Box
} from '@mui/material';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

const RecentActivityList = ({ activities = [] }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'success';
      case 'failed':
        return 'error';
      case 'running':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          최근 실행 기록
        </Typography>
        <List>
          {activities.map((activity, index) => (
            <ListItem 
              key={activity.id} 
              divider={index !== activities.length - 1}
              sx={{ py: 2 }}
            >
              <ListItemText
                primary={activity.name}
                secondary={formatDistanceToNow(new Date(activity.timestamp), { 
                  addSuffix: true,
                  locale: ko 
                })}
              />
              <Box>
                <Chip
                  label={activity.status}
                  color={getStatusColor(activity.status)}
                  size="small"
                />
              </Box>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default RecentActivityList; 