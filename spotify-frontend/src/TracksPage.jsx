import { useState, useEffect } from 'react';

export default function TracksPage() {
  const [tracks, setTracks] = useState([]);
  const [artist, setArtist] = useState('');
  const [album, setAlbum] = useState('');
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTracks();
  }, []);

  const fetchTracks = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', limit);
    if (artist) params.append('artist', artist);
    if (album) params.append('album', album);
    if (year) params.append('year', year);
    if (month) params.append('month', month);

    const response = await fetch(`http://localhost:8000/api/tracks?${params}`);
    const data = await response.json();
    setTracks(data);
    setLoading(false);
  };

  return (
    <div>
      <h1>Top Tracks</h1>
      
      <div>
        <input
          type="text"
          placeholder="Artist"
          value={artist}
          onChange={(e) => setArtist(e.target.value)}
        />
        <input
          type="text"
          placeholder="Album"
          value={album}
          onChange={(e) => setAlbum(e.target.value)}
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
        <button onClick={fetchTracks}>Search</button>
      </div>

      {loading && <p>Loading...</p>}

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Artist</th>
            <th>Track Name</th>
            <th>Streams</th>
          </tr>
        </thead>
        <tbody>
          {tracks.map((track, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{track.artist}</td>
              <td>{track.name}</td>
              <td>{track.stream_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}