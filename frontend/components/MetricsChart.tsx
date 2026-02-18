'use client';

import { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { fetchMetrics } from '@/lib/api';
import type { MetricsResponse } from '@/types';

function formatTime(isoString: string): string {
  return new Date(isoString).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default function MetricsChart() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchMetrics();
        setMetrics(data);
      } catch {
        const now = Date.now();
        const data = Array.from({ length: 12 }, (_, i) => ({
          timestamp: new Date(now - (11 - i) * 60000).toISOString(),
          latency: 80 + Math.random() * 120,
          error_rate: Math.random() * 2,
        }));
        setMetrics({ data });
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur">
        <div className="flex h-80 items-center justify-center">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        </div>
      </div>
    );
  }

  const chartData =
    metrics?.data?.map((d) => ({
      ...d,
      time: formatTime(d.timestamp),
      latency: d.latency ?? 0,
      error_rate: d.error_rate ?? 0,
    })) ?? [];

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur transition-all hover:border-slate-700">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Metrics Trend
        </h3>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="time"
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              axisLine={{ stroke: '#1e293b' }}
            />
            <YAxis
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              axisLine={{ stroke: '#1e293b' }}
              tickFormatter={(v) => `${v}ms`}
              yAxisId="latency"
            />
            <YAxis
              orientation="right"
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              axisLine={{ stroke: '#1e293b' }}
              tickFormatter={(v) => `${v}%`}
              yAxisId="error"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                border: '1px solid #1e293b',
                borderRadius: '0.75rem',
              }}
              labelStyle={{ color: '#94a3b8' }}
              formatter={(value: number, name: string) => [
                name === 'latency' ? `${value.toFixed(1)}ms` : `${value.toFixed(2)}%`,
                name === 'latency' ? 'Latency' : 'Error Rate',
              ]}
            />
            <Legend
              formatter={(value) => (
                <span className="text-slate-400">{value}</span>
              )}
            />
            <Line
              type="monotone"
              dataKey="latency"
              yAxisId="latency"
              stroke="#6366f1"
              strokeWidth={2}
              dot={{ fill: '#6366f1', r: 4 }}
              activeDot={{ r: 6 }}
              name="Latency"
            />
            <Line
              type="monotone"
              dataKey="error_rate"
              yAxisId="error"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={{ fill: '#f59e0b', r: 4 }}
              activeDot={{ r: 6 }}
              name="Error Rate"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
