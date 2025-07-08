import React from 'react';
import {
  Paper,
  Box,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
} from '@mui/material';

const PropertiesPanel = ({ selectedNode, onNodeUpdate }) => {
  if (!selectedNode) {
    return (
      <Paper sx={{ width: '100%', height: '100%', p: 2 }}>
        <Typography variant="body2" color="text.secondary">
          노드를 선택하여 속성을 편집하세요
        </Typography>
      </Paper>
    );
  }

  const renderAgentProperties = () => (
    <>
      <TextField
        fullWidth
        label="Agent 이름"
        value={selectedNode.data.name}
        onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, name: e.target.value } })}
        margin="normal"
      />
      <FormControl fullWidth margin="normal">
        <InputLabel>Agent 타입</InputLabel>
        <Select
          value={selectedNode.data.type}
          label="Agent 타입"
          onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, type: e.target.value } })}
        >
          <MenuItem value="image">이미지 생성</MenuItem>
          <MenuItem value="text">텍스트 분석</MenuItem>
        </Select>
      </FormControl>
      <FormControlLabel
        control={
          <Switch
            checked={selectedNode.data.enabled ?? true}
            onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, enabled: e.target.checked } })}
          />
        }
        label="활성화"
      />
    </>
  );

  const renderMcpToolProperties = () => (
    <>
      <TextField
        fullWidth
        label="도구 이름"
        value={selectedNode.data.name}
        onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, name: e.target.value } })}
        margin="normal"
      />
      <FormControl fullWidth margin="normal">
        <InputLabel>카테고리</InputLabel>
        <Select
          value={selectedNode.data.category}
          label="카테고리"
          onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, category: e.target.value } })}
        >
          <MenuItem value="search">검색</MenuItem>
          <MenuItem value="edit">편집</MenuItem>
        </Select>
      </FormControl>
    </>
  );

  const renderControlFlowProperties = () => (
    <>
      <TextField
        fullWidth
        label="노드 이름"
        value={selectedNode.data.name}
        onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, name: e.target.value } })}
        margin="normal"
      />
      <FormControl fullWidth margin="normal">
        <InputLabel>타입</InputLabel>
        <Select
          value={selectedNode.data.type}
          label="타입"
          onChange={(e) => onNodeUpdate({ ...selectedNode, data: { ...selectedNode.data, type: e.target.value } })}
        >
          <MenuItem value="condition">조건 분기</MenuItem>
          <MenuItem value="loop">반복</MenuItem>
        </Select>
      </FormControl>
    </>
  );

  return (
    <Paper sx={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          속성
        </Typography>

        {selectedNode.type === 'agent' && renderAgentProperties()}
        {selectedNode.type === 'mcpTool' && renderMcpToolProperties()}
        {selectedNode.type === 'controlFlow' && renderControlFlowProperties()}
      </Box>
    </Paper>
  );
};

export default PropertiesPanel; 