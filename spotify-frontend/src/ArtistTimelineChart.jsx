import { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { msToHours } from './utils';

// Same name always gives the same color
function colorFor(name) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = (hash * 31 + name.charCodeAt(i)) % 360;
  }
  return `hsl(${hash}, 70%, 60%)`;
}

// API shape: {buckets, series: [{artist, values}]}
// Recharts shape: [{bucket: "2022-01", s0: 175, s1: 86}, ...]
function toRows(timeline, metric) {
  return timeline.buckets.map((bucket, i) => {
    const row = { bucket };
    timeline.series.forEach((s, idx) => {
      const v = s.values[i];
      row[`s${idx}`] = v === null ? null : metric === 'time' ? msToHours(v) : v;
    });
    return row;
  });
}

const CustomTooltip = ({ active, payload, label, metric }) => {
  if (!active || !payload || payload.length === 0) return null;

  const entries = payload
    .filter((p) => p.value !== null && p.value !== undefined)
    .sort((a, b) => b.value - a.value);

  return (
    <div className="bg-gray-800 text-white px-3 py-2 rounded border border-gray-600">
      <div className="font-semibold mb-1">{label}</div>
      {entries.map((p) => (
        <div key={p.dataKey} style={{ color: p.color }}>
          {p.name}:{' '}
          {metric === 'time'
            ? `${Number(p.value).toFixed(1)} h`
            : p.value.toLocaleString()}
        </div>
      ))}
    </div>
  );
};

export default function ArtistTimelineChart({ timeline, metric, colors }) {
  const rows = useMemo(
    () => (timeline ? toRows(timeline, metric) : []),
    [timeline, metric]
  );

  if (!timeline || timeline.series.length === 0) {
    return <p className="text-white">No data to display</p>;
  }

  const colorOf = (artist) => colors?.[artist] ?? colorFor(artist);

  return (
    <ResponsiveContainer width="100%" height={500}>
      <LineChart data={rows} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
        <XAxis
          dataKey="bucket"
          tick={{ fill: '#fff', fontSize: 12 }}
          minTickGap={40}
        />
        <YAxis tick={{ fill: '#fff' }} />
        <Tooltip content={<CustomTooltip metric={metric} />} />
        <Legend wrapperStyle={{ color: '#fff' }} />
        {timeline.series.map((s, idx) => (
          <Line
            key={s.artist}
            type="monotone"
            dataKey={`s${idx}`}
            name={s.artist}
            stroke={colorOf(s.artist)}
            strokeWidth={2}
            dot={false}
            connectNulls={false}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}