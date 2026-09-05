import { useState, useEffect } from 'react';

export default function ArtistsPage() {
  const [artists, setArtists] = useState([]);
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchArtists();
  }, []);

  const fetchArtists = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', limit);
    if (year) params.append('year', year);
    if (month) params.append('month', month);

    const response = await fetch(`http://localhost:8000/api/artists?${params}`);
    const data = await response.json();
    setArtists(data);
    setLoading(false);
  };

  return (
    <div>
      <h1>Top Artists</h1>
      
      <div>
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
        <button onClick={fetchArtists}>Search</button>
      </div>

      {loading && <p>Loading...</p>}

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Artist</th>
            <th>Streams</th>
          </tr>
        </thead>
        <tbody>
          {artists.map((artist, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{artist.name}</td>
              <td>{artist.stream_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}