import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-gray-800 text-white px-2 py-1 rounded border border-gray-600">
        {payload[0].value.toLocaleString()}
      </div>
    );
  }
  return null;
};

export default function BarChartComponent({ data, dataKey, nameKey = 'name' }) {
  if (!data || data.length === 0) {
    return <p className="text-white">No data to display</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
        <XAxis 
          dataKey={nameKey} 
          angle={-45}
          textAnchor="end"
          height={100}
          tick={{ fill: '#fff', fontSize: 12 }}
        />
        <YAxis tick={{ fill: '#fff' }} />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey={dataKey} fill="#22c55e" />
      </BarChart>
    </ResponsiveContainer>
  );
}