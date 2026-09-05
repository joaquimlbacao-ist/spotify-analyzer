export default function SearchBar({ filters, onFilterChange }) {
  const handleChange = (key, value) => {
    onFilterChange({ ...filters, [key]: value });
  };

  const isTextInput = (key) => key === 'artist' || key === 'album';

  return (
    <div className="mb-6 p-4 bg-gray-700 rounded-lg flex justify-between items-center">
      <div className="flex flex-wrap gap-3">
        {Object.entries(filters).map(([key, value]) => {
          if (key === 'limit') return null;
          return (
            <input
              key={key}
              type={key === 'year' || key === 'month' ? 'number' : 'text'}
              placeholder={key.charAt(0).toUpperCase() + key.slice(1)}
              value={value || ''}
              onChange={(e) => handleChange(key, e.target.value)}
              className={`${
                isTextInput(key) ? 'w-56 px-3 py-2' : 'w-20 px-2 py-1 text-sm'
              } bg-gray-600 text-white rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500`}
            />
          );
        })}
      </div>
      
      <div className="flex items-center gap-2">
        <label className="text-white text-sm font-semibold">Limit:</label>
        <input
          type="number"
          value={filters.limit || ''}
          onChange={(e) => handleChange('limit', e.target.value)}
          className="w-20 px-2 py-1 text-sm bg-gray-600 text-white rounded focus:outline-none focus:ring-2 focus:ring-green-500"
        />
      </div>
    </div>
  );
}