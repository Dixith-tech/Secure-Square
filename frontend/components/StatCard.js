export default function StatCard({ icon, title, value, change, color }) {
  const colorMap = {
    red: 'bg-red-600 text-red-100 border-red-700',
    orange: 'bg-orange-600 text-orange-100 border-orange-700',
    green: 'bg-green-600 text-green-100 border-green-700',
    blue: 'bg-blue-600 text-blue-100 border-blue-700'
  };

  const bgColor = colorMap[color] || colorMap.blue;

  return (
    <div className={`${bgColor} p-6 rounded-xl border hover:shadow-lg transition`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium opacity-90 mb-2">{title}</p>
          <p className="text-3xl font-bold">{value}</p>
          <p className="text-xs mt-2 opacity-75">{change}</p>
        </div>
        <div className="opacity-50">
          {icon}
        </div>
      </div>
    </div>
  );
}
