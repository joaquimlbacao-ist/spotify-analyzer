import { useState } from 'react';

export default function FileUpload({ onUploadSuccess }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('bg-gray-600');
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('bg-gray-600');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('bg-gray-600');
    const droppedFiles = Array.from(e.dataTransfer.files).filter(f => f.name.endsWith('.json'));
    setFiles(droppedFiles);
  };

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files).filter(f => f.name.endsWith('.json'));
    setFiles(selectedFiles);
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Select at least one JSON file');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Upload failed');

      const data = await response.json();
      setMessage(`Uploaded ${data.count} streams successfully!`);
      setFiles([]);
      onUploadSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className="border-2 border-dashed border-gray-500 rounded-lg p-8 text-center bg-gray-800 cursor-pointer hover:bg-gray-700 transition"
      >
        <p className="text-white text-lg mb-2">Drag & drop your Spotify JSON files here</p>
        <p className="text-gray-400 text-sm mb-4">or</p>
        <label className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 cursor-pointer inline-block">
          Browse Files
          <input
            type="file"
            multiple
            accept=".json"
            onChange={handleFileSelect}
            className="hidden"
          />
        </label>
      </div>

      {files.length > 0 && (
        <div className="mt-6 p-4 bg-gray-700 rounded-lg">
          <h3 className="text-white font-semibold mb-3">Selected Files ({files.length})</h3>
          <ul className="space-y-2 mb-4">
            {files.map((file, idx) => (
              <li key={idx} className="text-gray-300 text-sm">{file.name}</li>
            ))}
          </ul>
          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-600"
          >
            {loading ? 'Uploading...' : 'Upload & Analyze'}
          </button>
        </div>
      )}

      {message && <p className="mt-4 p-3 bg-green-900 text-green-200 rounded">{message}</p>}
      {error && <p className="mt-4 p-3 bg-red-900 text-red-200 rounded">{error}</p>}
    </div>
  );
}