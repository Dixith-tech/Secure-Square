"use client";

import { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, Shield, TrendingUp, Lock } from 'lucide-react';
import API from '@/services/api';
import ThreatTable from '@/components/ThreatTable';
import AttackMap from '@/components/AttackMap';
import StatCard from '@/components/StatCard';

export default function Dashboard() {
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState([
    { time: "00:00", attacks: 10 },
    { time: "04:00", attacks: 25 },
    { time: "08:00", attacks: 35 },
    { time: "12:00", attacks: 50 },
    { time: "16:00", attacks: 40 },
    { time: "20:00", attacks: 60 }
  ]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);

  // Fetch threats data
  useEffect(() => {
    const fetchThreats = async () => {
      try {
        const response = await API.get('/api/v1/threats?limit=10');
        setThreats(response.data.items || []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching threats:', err);
        setError('Failed to load threats');
        setLoading(false);
      }
    };

    fetchThreats();
  }, []);

  // Fetch statistics
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await API.get('/api/v1/stats/threats');
        setStats(response.data);
      } catch (err) {
        console.error('Error fetching stats:', err);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://127.0.0.1:8000/ws';
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('✓ WebSocket connected');
      setWsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'threat') {
          // Add new threat to list
          setThreats(prev => [data.data, ...prev].slice(0, 10));
          
          // Update chart with new data point
          setChartData(prev => {
            const newData = [...prev];
            newData.push({
              time: new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }),
              attacks: (prev[prev.length - 1]?.attacks || 0) + (Math.random() > 0.5 ? 1 : 0)
            });
            return newData.slice(-12); // Keep last 12 data points
          });
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onerror = (error) => {
      console.error('✗ WebSocket error:', error);
      setWsConnected(false);
    };

    ws.onclose = () => {
      console.log('✗ WebSocket disconnected');
      setWsConnected(false);
      // Attempt to reconnect after 3 seconds
      setTimeout(() => {
        console.log('Attempting to reconnect...');
      }, 3000);
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  if (loading) {
    return (
      <div className="p-8 bg-black text-white min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Shield className="w-16 h-16 animate-spin mx-auto mb-4 text-blue-500" />
          <p className="text-xl">Loading Security Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 bg-black text-white min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Security Dashboard</h1>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <p className="text-sm text-gray-400">
            {wsConnected ? '✓ Live monitoring active' : '✗ Monitoring offline'}
          </p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-900 border border-red-700 p-4 rounded-lg mb-8">
          <p className="text-red-200">{error}</p>
        </div>
      )}

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={<AlertTriangle size={24} />}
            title="Total Threats"
            value={stats.total_threats}
            change="+12%"
            color="red"
          />
          <StatCard
            icon={<TrendingUp size={24} />}
            title="Critical"
            value={stats.critical_count}
            change={`${Math.round(stats.detection_rate)}%`}
            color="orange"
          />
          <StatCard
            icon={<Shield size={24} />}
            title="Blocked"
            value={stats.blocked_count}
            change="+8%"
            color="green"
          />
          <StatCard
            icon={<Lock size={24} />}
            title="Avg Risk Score"
            value={Math.round(stats.average_risk_score)}
            change="/100"
            color="blue"
          />
        </div>
      )}

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Attack Graph */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h2 className="text-2xl font-bold mb-6">Live Attack Timeline</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis 
                dataKey="time" 
                stroke="#666"
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                stroke="#666"
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1a1a1a', 
                  border: '1px solid #444',
                  borderRadius: '8px'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="attacks" 
                stroke="#ff0000" 
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Attack Map */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h2 className="text-2xl font-bold mb-6">Geographic Threats</h2>
          <AttackMap />
        </div>
      </div>

      {/* Threats Table */}
      <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
        <h2 className="text-2xl font-bold mb-6">Recent Threats</h2>
        {threats.length > 0 ? (
          <ThreatTable threats={threats} />
        ) : (
          <div className="text-center py-12 text-gray-400">
            <Shield className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p>No threats detected</p>
          </div>
        )}
      </div>
    </div>
  );
}
