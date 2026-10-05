import { useState, useMemo } from 'react';

export const PALETTE = [
  '#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#a855f7',
  '#06b6d4', '#ec4899', '#eab308', '#f97316', '#84cc16',
];
const MAX_ARTISTS = 10;

export default function ArtistPicker({ names, selected, onChange, noPlays }) {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);

  // Names are most-played first; matches that start with the query go on top
  const suggestions = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    const taken = new Set(selected.map((a) => a.name));
    return names
      .filter((n) => !taken.has(n) && n.toLowerCase().includes(q))
      .sort(
        (a, b) =>
          Number(b.toLowerCase().startsWith(q)) - Number(a.toLowerCase().startsWith(q))
      )
      .slice(0, 8);
  }, [query, names, selected]);

  const add = (name) => {
    // First palette color not already used by a chip; it stays with the artist
    const used = new Set(selected.map((a) => a.color));
    const color = PALETTE.find((c) => !used.has(c)) || PALETTE[0];
    onChange([...selected, { name, color }]);
    setQuery('');
    setOpen(false);
  };

  const remove = (name) => onChange(selected.filter((a) => a.name !== name));

  const full = selected.length >= MAX_ARTISTS;

  return (
    <div className="mb-4">
      <div className="relative max-w-md">
        <input
          type="text"
          value={query}
          disabled={full}
          placeholder={full ? `Maximum of ${MAX_ARTISTS} artists` : 'Search artist...'}
          onChange={(e) => {
            setQuery(e.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          onBlur={() => setOpen(false)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && suggestions[0]) add(suggestions[0]);
          }}
          className="w-full px-3 py-2 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {open && suggestions.length > 0 && (
          <ul className="absolute z-10 w-full mt-1 bg-gray-800 border border-gray-600 rounded shadow-lg">
            {suggestions.map((n) => (
              <li key={n}>
                <button
                  onMouseDown={(e) => {
                    e.preventDefault(); // keep the input focused
                    add(n);
                  }}
                  className="w-full text-left px-3 py-2 text-white hover:bg-gray-700"
                >
                  {n}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="flex flex-wrap gap-2 mt-3">
        {selected.map((a) => (
          <span
            key={a.name}
            title={noPlays?.has(a.name) ? 'No plays in this range' : undefined}
            className={`flex items-center gap-2 px-3 py-1 rounded-full bg-gray-700 text-white ${
              noPlays?.has(a.name) ? 'opacity-50' : ''
            }`}
          >
            <span
              className="inline-block w-3 h-3 rounded-full"
              style={{ backgroundColor: a.color }}
            />
            {a.name}
            <button
              onClick={() => remove(a.name)}
              aria-label={`Remove ${a.name}`}
              className="text-gray-300 hover:text-white"
            >
              ×
            </button>
          </span>
        ))}
      </div>
    </div>
  );
}
