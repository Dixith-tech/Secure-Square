import { AlertTriangle } from 'lucide-react';

export default function AlertPopup({ message, severity, onClose }) {
  const bgColor = {
    critical: 'bg-red-600',
    high: 'bg-orange-600',
    medium: 'bg-yellow-600',
    low: 'bg-blue-600'
  }[severity] || 'bg-gray-600';

  return (
    <div className={`${bgColor} text-white p-4 rounded-lg flex items-center gap-4 shadow-lg`}>
      <AlertTriangle size={24} />
      <div className="flex-1">
        <p className="font-bold">{severity.toUpperCase()}</p>
        <p>{message}</p>
      </div>
      <button
        onClick={onClose}
        className="text-white hover:text-gray-200 font-bold"
      >
        ✕
      </button>
    </div>
  );
}
