import { useState } from 'react';

export default function SearchBar({ filters, onFilterChange }) {
  const [showDateRange, setShowDateRange] = useState(false);

  const handleChange = (key, value) => {
    onFilterChange({ ...filters, [key]: value });
  };

  const isTextInput = (key) => key === 'artist' || key === 'album';
  const isNumberInput = (key) => ['year', 'month', 'limit'].includes(key);

  return (
    <div className="mb-6 p-4 bg-gray-700 rounded-lg flex items-center">
      <div className="flex justify-between items-center gap-4 w-full">
        <div className="flex flex-wrap gap-3 items-center">
          {Object.entries(filters).map(([key, value]) => {
            if (key === 'limit' || key === 'start_date' || key === 'end_date') return null;
            return (
              <input
                key={key}
                type={isNumberInput(key) ? 'number' : 'text'}
                placeholder={key.charAt(0).toUpperCase() + key.slice(1)}
                value={value || ''}
                onChange={(e) => handleChange(key, e.target.value)}
                className={`${
                  isTextInput(key) ? 'w-56' : key === 'month' ? 'w-28' : 'w-20'
                } px-3 py-2 bg-gray-600 text-white rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500`}
              />
            );
          })}
          
          <button
            onClick={() => setShowDateRange(!showDateRange)}
            className="px-3 py-2 bg-gray-600 text-gray-400 rounded hover:bg-gray-500 flex items-center gap-1 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
            Date Range
            <span className={`transition-transform ${showDateRange ? 'rotate-180' : ''}`}>▼</span>
            </button>
        </div>

        <div className="flex items-center gap-2 border-l border-gray-600 pl-4">
          <label className="text-white text-sm font-semibold">Limit:</label>
          <input
            type="number"
            value={filters.limit || ''}
            onChange={(e) => handleChange('limit', e.target.value)}
            className="w-20 px-3 py-2 bg-gray-600 text-white rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>
      </div>

      {showDateRange && (
        <div className="flex gap-3 pt-3 border-t border-gray-600">
          <input
            type="text"
            placeholder="Start Date (DD-MM-YYYY)"
            value={filters.start_date || ''}
            onChange={(e) => handleChange('start_date', e.target.value)}
            className="px-3 py-2 bg-gray-600 text-white rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <input
            type="text"
            placeholder="End Date (DD-MM-YYYY)"
            value={filters.end_date || ''}
            onChange={(e) => handleChange('end_date', e.target.value)}
            className="px-3 py-2 bg-gray-600 text-white rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>
      )}
    </div>
  );
}