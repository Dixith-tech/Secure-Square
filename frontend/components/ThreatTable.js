import { AlertCircle } from 'lucide-react';

export default function ThreatTable({ threats }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl">
      <h2 className="text-2xl font-bold mb-4">Recent Threats</h2>
      
      <table className="w-full text-left text-white">
        <thead className="border-b border-gray-700">
          <tr>
            <th className="pb-3">IP Address</th>
            <th className="pb-3">Threat Type</th>
            <th className="pb-3">Severity</th>
            <th className="pb-3">Location</th>
            <th className="pb-3">Device</th>
          </tr>
        </thead>
        <tbody>
          {threats && threats.map((threat, index) => (
            <tr key={index} className="border-b border-gray-800 hover:bg-gray-800">
              <td className="py-3">{threat.ip_address}</td>
              <td className="py-3 flex items-center gap-2">
                <AlertCircle size={16} />
                {threat.threat_type}
              </td>
              <td className="py-3">
                <span className={`px-2 py-1 rounded ${
                  threat.severity === 'Critical' ? 'bg-red-600' :
                  threat.severity === 'High' ? 'bg-orange-600' :
                  'bg-yellow-600'
                }`}>
                  {threat.severity}
                </span>
              </td>
              <td className="py-3">{threat.location}</td>
              <td className="py-3">{threat.device}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
