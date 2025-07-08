import React, { useState } from 'react';
import { Box } from '@mui/material';
import NodeLibrary from '../components/studio/NodeLibrary';
import WorkflowCanvas from '../components/studio/WorkflowCanvas';
import PropertiesPanel from '../components/studio/PropertiesPanel';

const Studio = () => {
  const [selectedNode, setSelectedNode] = useState(null);

  const handleNodeSelect = (node) => {
    setSelectedNode(node);
  };

  const handleNodeUpdate = (updatedNode) => {
    setSelectedNode(updatedNode);
    // TODO: 워크플로우 상태 업데이트 로직 추가
  };

  return (
    <Box sx={{ 
      display: 'flex', 
      height: 'calc(100vh - 64px)', // AppBar 높이 제외
      gap: 2,
      p: 2
    }}>
      {/* 좌측 패널: 노드 라이브러리 */}
      <Box sx={{ width: 300 }}>
        <NodeLibrary />
      </Box>

      {/* 중앙 패널: 워크플로우 캔버스 */}
      <Box sx={{ flexGrow: 1 }}>
        <WorkflowCanvas onNodeSelect={handleNodeSelect} />
      </Box>

      {/* 우측 패널: 속성 패널 */}
      <Box sx={{ width: 300 }}>
        <PropertiesPanel 
          selectedNode={selectedNode}
          onNodeUpdate={handleNodeUpdate}
        />
      </Box>
    </Box>
  );
};

export default Studio; 