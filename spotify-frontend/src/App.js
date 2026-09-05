import { useState } from 'react';
import ArtistsPage from './ArtistsPage';
import TracksPage from './TracksPage';
import AlbumsPage from './AlbumsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('artists');

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800">
      <div className="max-w-6xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold text-white mb-8">Spotify Analyzer</h1>
        
        <div className="flex gap-3 mb-8">
          <button 
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              currentPage === 'artists' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-700 text-gray-200 hover:bg-gray-600'
            }`}
            onClick={() => setCurrentPage('artists')}
          >
            Artists
          </button>
          <button 
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              currentPage === 'tracks' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-700 text-gray-200 hover:bg-gray-600'
            }`}
            onClick={() => setCurrentPage('tracks')}
          >
            Tracks
          </button>
          <button 
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              currentPage === 'albums' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-700 text-gray-200 hover:bg-gray-600'
            }`}
            onClick={() => setCurrentPage('albums')}
          >
            Albums
          </button>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          {currentPage === 'artists' && <ArtistsPage />}
          {currentPage === 'tracks' && <TracksPage />}
          {currentPage === 'albums' && <AlbumsPage />}
        </div>
      </div>
    </div>
  );
}

export default App;