export default function Table({ data, columns, columnLabels }) {
  if (!data || data.length === 0) {
    return <p className="text-white">No data found</p>;
  }

  return (
    <table className="w-full text-white mt-6">
      <thead className="bg-gray-700">
        <tr>
          <th className="px-4 py-2 text-left">#</th>
          {columnLabels.map((label) => (
            <th key={label} className="px-4 py-2 text-left">{label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index} className="border-b border-gray-700 hover:bg-gray-700">
            <td className="px-4 py-2">{index + 1}</td>
            {columns.map((col) => (
              <td key={col} className="px-4 py-2">
                {typeof row[col] === 'number' ? row[col].toLocaleString() : row[col]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}