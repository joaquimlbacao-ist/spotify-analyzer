export default function GridView({ data, imageKey, labelKey }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {data.map((item, idx) => (
        <div key={idx} className="flex flex-col items-center">
          <div
            className={`w-full aspect-square rounded-lg overflow-hidden ${
              !item[imageKey] ? 'bg-gray-600' : ''
            }`}
          >
            {item[imageKey] ? (
              <img
                src={item[imageKey]}
                alt={item[labelKey]}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No image
              </div>
            )}
          </div>
          <p className="mt-2 text-sm text-white text-center truncate w-full">
            {item[labelKey]}
          </p>
        </div>
      ))}
    </div>
  );
}