import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import SearchBar from './SearchBar';
import Table from './Table';

export default function AlbumsPage() {
  const [albums, setAlbums] = useState([]);
  const [filters, setFilters] = useState({
    artist: '',
    year: '',
    month: '',
    limit: 10
  });
  const [loading, setLoading] = useState(false);
  const debouncedFilters = useDebounce(filters, 500);

  useEffect(() => {
    fetchAlbums();
  }, [debouncedFilters]);

  const fetchAlbums = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', filters.limit);
    if (filters.artist) params.append('artist', filters.artist);
    if (filters.year) params.append('year', filters.year);
    if (filters.month) params.append('month', filters.month);

    const response = await fetch(`http://localhost:8000/api/albums?${params}`);
    const data = await response.json();
    setAlbums(data);
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Top Albums</h1>
      
      <SearchBar filters={filters} onFilterChange={setFilters} />
      
      {loading && <p className="text-white">Loading...</p>}
      
      <Table 
        data={albums} 
        columns={['artist', 'name', 'stream_count']}
        columnLabels={['Artist', 'Album', 'Streams']}
      />
    </div>
  );
}