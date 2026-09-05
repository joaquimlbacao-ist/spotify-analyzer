import { useState, useEffect } from 'react';

export default function AlbumsPage() {
  const [albums, setAlbums] = useState([]);
  const [artist, setArtist] = useState('');
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAlbums();
  }, []);

  const fetchAlbums = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', limit);
    if (artist) params.append('artist', artist);
    if (year) params.append('year', year);
    if (month) params.append('month', month);

    const response = await fetch(`http://localhost:8000/api/albums?${params}`);
    const data = await response.json();
    setAlbums(data);
    setLoading(false);
  };

  return (
    <div>
      <h1>Top Albums</h1>
      
      <div>
        <input
          type="text"
          placeholder="Artist"
          value={artist}
          onChange={(e) => setArtist(e.target.value)}
        />
        <input
          type="number"
          placeholder="Year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />
        <input
          type="number"
          placeholder="Month (1-12)"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
        <input
          type="number"
          placeholder="Limit"
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
        />
        <button onClick={fetchAlbums}>Search</button>
      </div>

      {loading && <p>Loading...</p>}

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Streams</th>
          </tr>
        </thead>
        <tbody>
          {albums.map((album, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{album.artist}</td>
              <td>{album.name}</td>
              <td>{album.stream_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}