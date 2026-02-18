'use client';

import { useEffect, useState } from 'react';
import { fetchLatestRiskScore } from '@/lib/api';
import type { RiskScore } from '@/types';

function getGaugeColor(score: number): string {
  if (score <= 30) return '#10b981';
  if (score <= 60) return '#f59e0b';
  return '#ef4444';
}

export default function RiskGauge() {
  const [riskScore, setRiskScore] = useState<RiskScore | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchLatestRiskScore();
        setRiskScore(data);
      } catch {
        setRiskScore({ score: 42, decision: 'manual_review' });
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur">
        <div className="flex h-48 items-center justify-center">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        </div>
      </div>
    );
  }

  const score = riskScore?.score ?? 0;
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  const color = getGaugeColor(score);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur transition-all hover:border-slate-700">
      <p className="mb-4 text-center text-sm font-medium uppercase tracking-wider text-slate-400">
        Risk Gauge
      </p>
      <div className="relative mx-auto flex h-48 w-48 items-center justify-center">
        <svg
          className="-rotate-90"
          width="180"
          height="180"
          viewBox="0 0 180 180"
          aria-label="Risk score gauge"
        >
          {/* Background track */}
          <circle
            cx="90"
            cy="90"
            r="45"
            fill="none"
            stroke="#1e293b"
            strokeWidth="12"
          />
          {/* Progress arc - animated */}
          <circle
            cx="90"
            cy="90"
            r="45"
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="text-3xl font-bold tabular-nums"
            style={{ color }}
          >
            {Math.round(score)}
          </span>
          <span className="text-xs text-slate-500">/ 100</span>
        </div>
      </div>
      <div className="mt-2 flex justify-between text-xs text-slate-500">
        <span>Low</span>
        <span>Medium</span>
        <span>High</span>
      </div>
    </div>
  );
}
