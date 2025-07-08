import React from 'react';
import { Box, AppBar, Toolbar, Typography, IconButton, Avatar, Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Dashboard, Code, AccountTree, Storage, Settings, Logout } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const DRAWER_WIDTH = 240;

const menuItems = [
  { text: '대시보드', icon: <Dashboard />, path: '/' },
  { text: 'AI Agents', icon: <Code />, path: '/agents' },
  { text: '워크플로우', icon: <AccountTree />, path: '/workflows' },
  { text: 'MCP 서버', icon: <Storage />, path: '/mcp' },
  { text: '설정', icon: <Settings />, path: '/settings' },
];

const AuthenticatedLayout = ({ children }) => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            AI Agent Builder
          </Typography>
          <IconButton color="inherit">
            <Avatar sx={{ width: 32, height: 32 }} />
          </IconButton>
        </Toolbar>
      </AppBar>
      
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem button key={item.text} onClick={() => navigate(item.path)}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
            <ListItem button>
              <ListItemIcon><Logout /></ListItemIcon>
              <ListItemText primary="로그아웃" />
            </ListItem>
          </List>
        </Box>
      </Drawer>
      
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default AuthenticatedLayout; 