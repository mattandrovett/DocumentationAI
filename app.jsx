import React, { useState } from 'react';
import axios from 'axios';
import { UnControlled as CodeMirror } from 'react-codemirror2';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/material.css';

function App() {
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/process-code', { code });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert('Error processing code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Code Assistant</h1>
      <CodeMirror
        value={code}
        options={{
          mode: 'python',
          theme: 'material',
          lineNumbers: true,
        }}
        onChange={(editor, data, value) => setCode(value)}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Process Code'}
      </button>
      {result && (
        <div>
          <h2>Commented Code</h2>
          <CodeMirror
            value={result.commented_code}
            options={{
              mode: 'python',
              theme: 'material',
              lineNumbers: true,
              readOnly: true,
            }}
          />
          <h2>Documentation</h2>
          <pre>{result.documentation}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
