import { useState } from 'react';
import FileUpload from './FileUpload';
import ArtistsPage from './ArtistsPage';
import TracksPage from './TracksPage';
import AlbumsPage from './AlbumsPage';

export default function App() {
  const [dataLoaded, setDataLoaded] = useState(false);
  const [activePage, setActivePage] = useState('artists');

  const handleUploadSuccess = () => {
    setDataLoaded(true);
  };

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
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-white">Spotify Analyzer</h1>
          <button
            onClick={() => setDataLoaded(false)}
            className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
          >
            Upload New Data
          </button>
        </div>

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
      </div>
    </div>
  );
}