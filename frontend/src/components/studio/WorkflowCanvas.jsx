import React, { useState, useCallback } from 'react';
import ReactFlow, {
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Box, Paper, IconButton, TextField } from '@mui/material';
import { Save, PlayArrow } from '@mui/icons-material';

// 노드 스타일 정의
const nodeTypes = {
  agent: ({ data }) => (
    <div style={{ 
      padding: '10px',
      borderRadius: '5px',
      background: '#e3f2fd',
      border: '1px solid #90caf9'
    }}>
      <div style={{ fontWeight: 'bold' }}>{data.name}</div>
      <div style={{ fontSize: '0.8em' }}>Agent</div>
    </div>
  ),
  mcpTool: ({ data }) => (
    <div style={{ 
      padding: '10px',
      borderRadius: '5px',
      background: '#f3e5f5',
      border: '1px solid #ce93d8'
    }}>
      <div style={{ fontWeight: 'bold' }}>{data.name}</div>
      <div style={{ fontSize: '0.8em' }}>MCP Tool</div>
    </div>
  ),
  controlFlow: ({ data }) => (
    <div style={{ 
      padding: '10px',
      borderRadius: '5px',
      background: '#fff3e0',
      border: '1px solid #ffb74d'
    }}>
      <div style={{ fontWeight: 'bold' }}>{data.name}</div>
      <div style={{ fontSize: '0.8em' }}>Control Flow</div>
    </div>
  ),
};

const WorkflowCanvas = ({ onNodeSelect }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [workflowName, setWorkflowName] = useState('새 워크플로우');

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const reactFlowBounds = event.target.getBoundingClientRect();
      const data = JSON.parse(event.dataTransfer.getData('application/reactflow'));
      
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };

      const newNode = {
        id: `${data.type}-${Date.now()}`,
        type: data.type,
        position,
        data: data.data,
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [setNodes]
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onNodeClick = useCallback((event, node) => {
    onNodeSelect(node);
  }, [onNodeSelect]);

  return (
    <Paper 
      sx={{ 
        width: '100%', 
        height: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      <Box sx={{ 
        p: 1, 
        display: 'flex', 
        alignItems: 'center',
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <TextField
          value={workflowName}
          onChange={(e) => setWorkflowName(e.target.value)}
          variant="standard"
          sx={{ flexGrow: 1, mr: 2 }}
        />
        <IconButton color="primary">
          <Save />
        </IconButton>
        <IconButton color="success">
          <PlayArrow />
        </IconButton>
      </Box>

      <Box sx={{ flexGrow: 1 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </Box>
    </Paper>
  );
};

export default WorkflowCanvas; 