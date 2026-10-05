const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const ARTIST_OPTIONS = [3, 5, 10, 15, 20];

const pad = (n) => String(n).padStart(2, '0');

const selectClass =
  'px-3 py-2 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-green-500';

// Picker state -> DD-MM-YYYY strings for the API
export function rangeToDates(r) {
  const startMonth = r.mode === 'year' ? 1 : r.startMonth;
  const endMonth = r.mode === 'year' ? 12 : r.endMonth;
  const lastDay = new Date(r.endYear, endMonth, 0).getDate();
  return {
    start_date: `01-${pad(startMonth)}-${r.startYear}`,
    end_date: `${pad(lastDay)}-${pad(endMonth)}-${r.endYear}`,
  };
}

export function isRangeValid(r) {
  const start = r.startYear * 12 + (r.mode === 'year' ? 1 : r.startMonth);
  const end = r.endYear * 12 + (r.mode === 'year' ? 12 : r.endMonth);
  return start <= end;
}

export default function TimelineControls({ value, onChange, minYear, maxYear, showTop = true }) {
  const years = [];
  for (let y = minYear; y <= maxYear; y++) years.push(y);

  const isMonth = value.mode === 'month';
  const set = (patch) => onChange({ ...value, ...patch });

  const yearSelect = (field) => (
    <select
      value={value[field]}
      onChange={(e) => set({ [field]: Number(e.target.value) })}
      className={selectClass}
    >
      {years.map((y) => (
        <option key={y} value={y}>{y}</option>
      ))}
    </select>
  );

  const monthSelect = (field) => (
    <select
      value={value[field]}
      onChange={(e) => set({ [field]: Number(e.target.value) })}
      className={selectClass}
    >
      {MONTHS.map((m, i) => (
        <option key={m} value={i + 1}>{m}</option>
      ))}
    </select>
  );

  const modeButton = (mode, label) => (
    <button
      onClick={() => set({ mode })}
      className={`px-4 py-2 rounded ${
        value.mode === mode ? 'bg-green-500 text-white' : 'bg-gray-700 text-gray-200'
      }`}
    >
      {label}
    </button>
  );

  return (
    <div className="mb-4">
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex gap-2">
          {modeButton('year', 'By year')}
          {modeButton('month', 'By month')}
        </div>

        <div className="flex items-center gap-2">
          <label className="text-white font-semibold">From:</label>
          {isMonth && monthSelect('startMonth')}
          {yearSelect('startYear')}
        </div>

        <div className="flex items-center gap-2">
          <label className="text-white font-semibold">To:</label>
          {isMonth && monthSelect('endMonth')}
          {yearSelect('endYear')}
        </div>

        {showTop && (
          <div className="flex items-center gap-2">
            <label className="text-white font-semibold">Artists:</label>
            <select
              value={value.top}
              onChange={(e) => set({ top: Number(e.target.value) })}
              className={selectClass}
            >
              {ARTIST_OPTIONS.map((n) => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {!isRangeValid(value) && (
        <p className="text-red-400 mt-2">The start of the range must be before the end.</p>
      )}
    </div>
  );
}