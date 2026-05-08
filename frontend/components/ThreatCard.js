import { AlertCircle } from 'lucide-react';

export default function ThreatCard({ ip, threat, severity, icon }) {
  const severityColor = {
    Critical: 'bg-red-600',
    High: 'bg-orange-600',
    Medium: 'bg-yellow-600',
    Low: 'bg-blue-600'
  }[severity] || 'bg-gray-600';

  return (
    <div className="bg-gray-900 p-4 rounded-lg border border-gray-700 hover:border-blue-500 transition">
      <div className="flex items-center justify-between mb-2">
        <p className="text-gray-400 text-sm">IP: {ip}</p>
        <AlertCircle size={20} className="text-red-500" />
      </div>
      <p className="text-white font-bold mb-2">{threat}</p>
      <span className={`px-2 py-1 rounded text-sm text-white ${severityColor}`}>
        {severity}
      </span>
    </div>
  );
}
