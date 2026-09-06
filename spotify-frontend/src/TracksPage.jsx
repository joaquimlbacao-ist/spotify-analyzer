import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import SearchBar from './SearchBar';
import Table from './Table';
import BarChartComponent from './BarChart';

export default function TracksPage() {
  const [tracks, setTracks] = useState([]);
  const [filters, setFilters] = useState({
    artist: '',
    album: '',
    year: '',
    month: '',
    limit: 10
  });
  const [loading, setLoading] = useState(false);
  const [viewType, setViewType] = useState('table');
  const debouncedFilters = useDebounce(filters, 500);

  useEffect(() => {
    fetchTracks();
  }, [debouncedFilters]);

  const fetchTracks = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', filters.limit);
    if (filters.artist) params.append('artist', filters.artist);
    if (filters.album) params.append('album', filters.album);
    if (filters.year) params.append('year', filters.year);
    if (filters.month) params.append('month', filters.month);

    const response = await fetch(`http://localhost:8000/api/tracks?${params}`);
    const data = await response.json();
    setTracks(data);
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Top Tracks</h1>
      
      <SearchBar filters={filters} onFilterChange={setFilters} />
      
      <div className="flex gap-2 mb-4">
        <button 
          onClick={() => setViewType('table')}
          className={`px-4 py-2 rounded ${viewType === 'table' ? 'bg-green-500 text-white' : 'bg-gray-700 text-gray-200'}`}
        >
          Table
        </button>
        <button 
          onClick={() => setViewType('chart')}
          className={`px-4 py-2 rounded ${viewType === 'chart' ? 'bg-green-500 text-white' : 'bg-gray-700 text-gray-200'}`}
        >
          Chart
        </button>
      </div>
      
      {loading && <p className="text-white">Loading...</p>}
      
      {viewType === 'table' ? (
        <Table 
          data={tracks} 
          columns={['artist', 'name', 'stream_count']}
          columnLabels={['Artist', 'Track', 'Streams']}
        />
      ) : (
        <BarChartComponent data={tracks} dataKey="stream_count" nameKey="name" />
      )}
    </div>
  );
}