import { useState, useEffect } from 'react';
import FileUpload from './FileUpload';
import ArtistsPage from './ArtistsPage';
import TracksPage from './TracksPage';
import AlbumsPage from './AlbumsPage';

export default function App() {
  const [dataLoaded, setDataLoaded] = useState(false);
  const [activePage, setActivePage] = useState('artists');
  const [streamInfo, setStreamInfo] = useState(null);
  const [showDataModal, setShowDataModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uploadMode, setUploadMode] = useState(false);

  // Check if data exists on mount
  useEffect(() => {
    checkData();
  }, []);

  const checkData = async () => {
    try {
      const API_URL = process.env.REACT_APP_API_URL;
      const response = await fetch(`${API_URL}/api/has-data`);
      const data = await response.json();
      setDataLoaded(data.has_streams);
      if (data.has_streams) {
        fetchStreamInfo();
      }
    } catch (e) {
      console.error('Error checking data:', e);
    } finally {
      setLoading(false);
    }
  };

  const fetchStreamInfo = async () => {
    try {
      const API_URL = process.env.REACT_APP_API_URL;
      const response = await fetch(`${API_URL}/api/stream-info`);
      const data = await response.json();
      setStreamInfo(data);
    } catch (e) {
      console.error('Error fetching stream info:', e);
    }
  };

  const handleUploadSuccess = () => {
    setDataLoaded(true);
    setShowDataModal(false);
    checkData();
  };

  const handleDeleteStreams = async () => {
    if (!window.confirm('Are you sure? This will delete all streams permanently.')) {
      return;
    }
    try {
      const API_URL = process.env.REACT_APP_API_URL;
      await fetch(`${API_URL}/api/streams`, { method: 'DELETE' });
      setDataLoaded(false);
      setStreamInfo(null);
    } catch (e) {
      console.error('Error deleting streams:', e);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8 flex items-center justify-center">
        <p className="text-white text-xl">Loading...</p>
      </div>
    );
  }

  if (!dataLoaded) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8">
        <h1 className="text-4xl font-bold text-white text-center mb-8">Spotify Analyzer</h1>
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8">
      <div className="max-w-7xl mx-auto">
        {uploadMode ? (
          <FileUpload onUploadSuccess={() => {
            setUploadMode(false);
            checkData();
          }} />
        ) : (
          <>
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-4xl font-bold text-white">Spotify Analyzer</h1>
              <button
                onClick={() => setShowDataModal(!showDataModal)}
                className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
              >
                Manage Data
              </button>
            </div>

            {showDataModal && (
              <div className="mb-6 p-4 bg-gray-800 rounded border border-gray-600">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-white font-semibold">Stream Count: {streamInfo?.count}</p>
                    <p className="text-gray-400 text-sm">
                      {streamInfo?.min_date} to {streamInfo?.max_date}
                    </p>
                  </div>
                  <button
                    onClick={() => setShowDataModal(false)}
                    className="text-gray-400 hover:text-white"
                  >
                    ✕
                  </button>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => setUploadMode(true)}
                    className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    Upload More Files
                  </button>
                  <button
                    onClick={handleDeleteStreams}
                    className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                  >
                    Delete All Streams
                  </button>
                </div>
              </div>
            )}

            <div className="flex gap-4 mb-8 border-b border-gray-600">
              {['artists', 'tracks', 'albums'].map(page => (
                <button
                  key={page}
                  onClick={() => setActivePage(page)}
                  className={`px-4 py-2 font-semibold transition ${
                    activePage === page
                      ? 'text-green-500 border-b-2 border-green-500'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  {page.charAt(0).toUpperCase() + page.slice(1)}
                </button>
              ))}
            </div>

            {activePage === 'artists' && <ArtistsPage />}
            {activePage === 'tracks' && <TracksPage />}
            {activePage === 'albums' && <AlbumsPage />}
          </>
        )}
      </div>
    </div>
  );
}