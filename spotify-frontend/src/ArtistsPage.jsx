import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import SearchBar from './SearchBar';
import Table from './Table';
import BarChartComponent from './BarChart';
import { formatMs, msToHours } from './utils';
import ArtistTimelineChart from './ArtistTimelineChart';
import TimelineControls, { rangeToDates, isRangeValid } from './TimelineControls';

export default function ArtistsPage() {
  const [artists, setArtists] = useState([]);
  const [filters, setFilters] = useState({
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
  const [timeline, setTimeline] = useState(null);
  const [yearBounds, setYearBounds] = useState(null);
  const [timelineRange, setTimelineRange] = useState(null);

  useEffect(() => {
    fetchArtists();
  }, [debouncedFilters, metric]);

  const fetchArtists = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('limit', filters.limit);
    params.append('sort_by', metric);
    if (filters.year) params.append('year', filters.year);
    if (filters.month) params.append('month', filters.month);
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);

    const API_URL = process.env.REACT_APP_API_URL;
    const response = await fetch(`${API_URL}/api/artists?${params}`);
    const data = await response.json();
    setArtists(data);
    setLoading(false);
  };

  useEffect(() => {
      if (viewType === 'timeline' && timelineRange && isRangeValid(timelineRange)) {
        fetchTimeline();
      }
    }, [timelineRange, metric, viewType]);

  const fetchTimeline = async () => {
    setLoading(true);
    const { start_date, end_date } = rangeToDates(timelineRange);
    const params = new URLSearchParams({
      top: timelineRange.top,
      metric,
      start_date,
      end_date,
      bucket: timelineRange.mode === 'year' ? 'year' : 'month',
    });

    const API_URL = process.env.REACT_APP_API_URL;
    const response = await fetch(`${API_URL}/api/artists/timeline?${params}`);
    const data = await response.json();
    setTimeline(data);
    setLoading(false);
  };

  useEffect(() => {
    const loadBounds = async () => {
      const API_URL = process.env.REACT_APP_API_URL;
      const res = await fetch(`${API_URL}/api/stream-info`);
      const info = await res.json();
      if (!info.min_date || !info.max_date) return;

      const min = Number(String(info.min_date).match(/\d{4}/)[0]);
      const max = Number(String(info.max_date).match(/\d{4}/)[0]);
      setYearBounds({ min, max });
      setTimelineRange({
        mode: 'year',
        year: max,
        startYear: min,
        startMonth: 1,
        endYear: max,
        endMonth: 12,
        top: 5,
      });
    };
    loadBounds();
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Top Artists</h1>
      
      {viewType !== 'timeline' && (
        <SearchBar filters={filters} onFilterChange={setFilters} />
      )}

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
          <button 
            onClick={() => setViewType('timeline')}
            className={`px-4 py-2 rounded ${viewType === 'timeline' ? 'bg-green-500 text-white' : 'bg-gray-700 text-gray-200'}`}
          >
            Timeline
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

      {viewType === 'timeline' && timelineRange && yearBounds && (
        <TimelineControls
          value={timelineRange}
          onChange={setTimelineRange}
          minYear={yearBounds.min}
          maxYear={yearBounds.max}
        />
      )}

      {loading && <p className="text-white">Loading...</p>}

      {viewType === 'table' ? (
        <Table 
          data={artists.map(a => ({
            ...a,
            display_value: metric === 'time' ? formatMs(a.total_ms) : a.stream_count
          }))} 
          columns={['name', 'display_value']}
          columnLabels={['Artist', metric === 'time' ? 'Total Time' : 'Streams']}
        />
      ) : viewType === 'chart' ? (
        <BarChartComponent 
          data={metric === 'time' ? artists.map(a => ({...a, display_value: msToHours(a.total_ms)})) : artists} 
          dataKey={metric === 'time' ? 'display_value' : 'stream_count'}
          nameKey="name" 
        />
      ) : (
        <ArtistTimelineChart timeline={timeline} metric={metric} />
      )}
    </div>
  );
}