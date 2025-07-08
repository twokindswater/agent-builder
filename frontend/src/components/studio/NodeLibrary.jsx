import React from 'react';
import { 
  Box, 
  Typography, 
  Accordion, 
  AccordionSummary, 
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper
} from '@mui/material';
import { ExpandMore, SmartToy, Build, AccountTree } from '@mui/icons-material';

// 임시 데이터
const mockAgents = [
  { id: 1, name: '이미지 생성 Agent', type: 'image' },
  { id: 2, name: '텍스트 분석 Agent', type: 'text' },
];

const mockMcpTools = [
  { id: 1, name: 'File Search', category: 'search' },
  { id: 2, name: 'Code Edit', category: 'edit' },
];

const mockControlFlows = [
  { id: 1, name: 'If/Else', type: 'condition' },
  { id: 2, name: 'For Loop', type: 'loop' },
];

const NodeLibrary = () => {
  const onDragStart = (event, nodeType, data) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify({
      type: nodeType,
      data
    }));
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <Paper sx={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          노드 라이브러리
        </Typography>

        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>AI Agents</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <List>
              {mockAgents.map((agent) => (
                <ListItem
                  key={agent.id}
                  draggable
                  onDragStart={(e) => onDragStart(e, 'agent', agent)}
                  sx={{ cursor: 'grab' }}
                >
                  <ListItemIcon>
                    <SmartToy />
                  </ListItemIcon>
                  <ListItemText primary={agent.name} />
                </ListItem>
              ))}
            </List>
          </AccordionDetails>
        </Accordion>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>MCP Tools</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <List>
              {mockMcpTools.map((tool) => (
                <ListItem
                  key={tool.id}
                  draggable
                  onDragStart={(e) => onDragStart(e, 'mcpTool', tool)}
                  sx={{ cursor: 'grab' }}
                >
                  <ListItemIcon>
                    <Build />
                  </ListItemIcon>
                  <ListItemText primary={tool.name} />
                </ListItem>
              ))}
            </List>
          </AccordionDetails>
        </Accordion>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>Control Flow</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <List>
              {mockControlFlows.map((flow) => (
                <ListItem
                  key={flow.id}
                  draggable
                  onDragStart={(e) => onDragStart(e, 'controlFlow', flow)}
                  sx={{ cursor: 'grab' }}
                >
                  <ListItemIcon>
                    <AccountTree />
                  </ListItemIcon>
                  <ListItemText primary={flow.name} />
                </ListItem>
              ))}
            </List>
          </AccordionDetails>
        </Accordion>
      </Box>
    </Paper>
  );
};

export default NodeLibrary; 