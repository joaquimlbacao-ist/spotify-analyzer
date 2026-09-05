import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import SearchBar from './SearchBar';
import Table from './Table';

export default function ArtistsPage() {
  const [artists, setArtists] = useState([]);
  const [filters, setFilters] = useState({
    year: '',
    month: '',
    limit: 10
  });
  const [loading, setLoading] = useState(false);
  const debouncedFilters = useDebounce(filters, 500);

  useEffect(() => {
    fetchArtists();
  }, [debouncedFilters]);

  const fetchArtists = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', filters.limit);
    if (filters.year) params.append('year', filters.year);
    if (filters.month) params.append('month', filters.month);

    const response = await fetch(`http://localhost:8000/api/artists?${params}`);
    const data = await response.json();
    setArtists(data);
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Top Artists</h1>
      
      <SearchBar filters={filters} onFilterChange={setFilters} />
      
      {loading && <p className="text-white">Loading...</p>}
      
      <Table 
        data={artists} 
        columns={['name', 'stream_count']}
        columnLabels={['Artist', 'Streams']}
      />
    </div>
  );
}