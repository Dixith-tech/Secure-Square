import { LineChart, Line, AreaChart, Area, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function LiveChart({ data, title, dataKey }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl">
      <h3 className="text-xl font-bold text-white mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" stroke="#888" />
          <YAxis stroke="#888" />
          <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #444' }} />
          <Area type="monotone" dataKey={dataKey} stroke="#ff0000" fill="#ff0000" fillOpacity={0.3} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
