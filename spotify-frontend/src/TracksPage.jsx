import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import SearchBar from './SearchBar';
import Table from './Table';
import BarChartComponent from './BarChart';
import { formatMs, msToHours } from './utils';

export default function TracksPage() {
  const [tracks, setTracks] = useState([]);
  const [filters, setFilters] = useState({
    artist: '',
    album: '',
    year: '',
    month: '',
    start_date: '',
    end_date: '',
    limit: 10
  });
  const [loading, setLoading] = useState(false);
  const [viewType, setViewType] = useState('table');
  const [metric, setMetric] = useState('streams');
  const debouncedFilters = useDebounce(filters, 500);

  useEffect(() => {
    fetchTracks();
  }, [debouncedFilters, metric]);

  const fetchTracks = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', filters.limit);
    params.append('sort_by', metric);
    if (filters.artist) params.append('artist', filters.artist);
    if (filters.album) params.append('album', filters.album);
    if (filters.year) params.append('year', filters.year);
    if (filters.month) params.append('month', filters.month);
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);

    const response = await fetch(`http://localhost:8000/api/tracks?${params}`);
    const data = await response.json();
    setTracks(data);
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Top Tracks</h1>
      
      <SearchBar 
        filters={filters} 
        onFilterChange={setFilters}
      />

      <div className="flex gap-2 mb-4 justify-between items-center">
        <div className="flex gap-2">
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

        <div className="flex items-center gap-2">
          <label className="text-white font-semibold">Sort by:</label>
          <select 
            value={metric}
            onChange={(e) => setMetric(e.target.value)}
            className="px-4 py-2 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="streams">Streams</option>
            <option value="time">Time</option>
          </select>
        </div>
      </div>

      {loading && <p className="text-white">Loading...</p>}

      {viewType === 'table' ? (
        <Table 
          data={tracks.map(t => ({
            ...t,
            display_value: metric === 'time' ? formatMs(t.total_ms) : t.stream_count
          }))} 
          columns={['artist', 'name', 'display_value']}
          columnLabels={['Artist', 'Track', metric === 'time' ? 'Total Time' : 'Streams']}
        />
      ) : (
        <BarChartComponent 
          data={metric === 'time' ? tracks.map(a => ({...a, display_value: msToHours(a.total_ms)})) : tracks} 
          dataKey={metric === 'time' ? 'display_value' : 'stream_count'}
          nameKey="name" 
        />
      )}
    </div>
  );
}