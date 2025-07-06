import React from 'react';

const AgentCreator = () => {
  return (
    <div className="agent-creator">
      <h1>Create a New AI Agent</h1>
      <form>
        <div>
          <label htmlFor="template">Template:</label>
          <select id="template" name="template">
            <option value="chatbot">Chatbot</option>
            <option value="data-analysis">Data Analysis</option>
            <option value="creative">Creative</option>
          </select>
        </div>
        <div>
          <label htmlFor="name">Agent Name:</label>
          <input type="text" id="name" name="name" required />
        </div>
        <div>
          <label htmlFor="description">Description:</label>
          <textarea id="description" name="description"></textarea>
        </div>
        <button type="submit">Create Agent</button>
      </form>
    </div>
  );
};

export default AgentCreator; 