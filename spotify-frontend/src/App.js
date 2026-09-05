import { useState } from 'react';
import ArtistsPage from './ArtistsPage';
import TracksPage from './TracksPage';
import AlbumsPage from './AlbumsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('artists');

  return (
    <div>
      <h1>Spotify Analyzer</h1>
      
      <div>
        <button onClick={() => setCurrentPage('artists')}>Artists</button>
        <button onClick={() => setCurrentPage('tracks')}>Tracks</button>
        <button onClick={() => setCurrentPage('albums')}>Albums</button>
      </div>

      {currentPage === 'artists' && <ArtistsPage />}
      {currentPage === 'tracks' && <TracksPage />}
      {currentPage === 'albums' && <AlbumsPage />}
    </div>
  );
}

export default App;