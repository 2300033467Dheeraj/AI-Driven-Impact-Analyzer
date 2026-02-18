'use client';

import { useEffect, useState } from 'react';
import { fetchLatestRiskScore } from '@/lib/api';
import type { RiskScore } from '@/types';
import DecisionBadge from './DecisionBadge';
import { AlertTriangle } from 'lucide-react';

function getRiskColor(score: number): string {
  if (score <= 30) return 'text-emerald-400';
  if (score <= 60) return 'text-amber-400';
  return 'text-red-400';
}

function getRiskBgGlow(score: number): string {
  if (score <= 30) return 'shadow-emerald-500/20';
  if (score <= 60) return 'shadow-amber-500/20';
  return 'shadow-red-500/20';
}

export default function RiskCard() {
  const [riskScore, setRiskScore] = useState<RiskScore | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchLatestRiskScore();
        setRiskScore(data);
      } catch (err) {
        setError('Failed to fetch risk score');
        setRiskScore({
          score: 42,
          decision: 'manual_review',
          timestamp: new Date().toISOString(),
        });
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-8 shadow-xl backdrop-blur">
        <div className="flex items-center justify-center py-16">
          <div className="h-12 w-12 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        </div>
      </div>
    );
  }

  if (!riskScore) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-8 shadow-xl backdrop-blur">
        <div className="flex flex-col items-center gap-3 text-slate-400">
          <AlertTriangle className="h-12 w-12" />
          <p>No risk data available</p>
        </div>
      </div>
    );
  }

  const score = riskScore.score;
  const colorClass = getRiskColor(score);
  const glowClass = getRiskBgGlow(score);

  return (
    <div
      className={`rounded-2xl border border-slate-800 bg-slate-900/50 p-8 shadow-xl backdrop-blur transition-all hover:shadow-2xl ${glowClass}`}
    >
      {error && (
        <p className="mb-3 text-sm text-amber-500">Using fallback data</p>
      )}
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium uppercase tracking-wider text-slate-400">
            Current Risk Score
          </p>
          <p className={`mt-2 text-6xl font-bold tabular-nums ${colorClass}`}>
            {Math.round(score)}
          </p>
          <p className="mt-1 text-xs text-slate-500">out of 100</p>
        </div>
        <DecisionBadge decision={riskScore.decision} size="lg" />
      </div>
      {riskScore.timestamp && (
        <p className="mt-4 text-xs text-slate-500">
          Last updated: {new Date(riskScore.timestamp).toLocaleString()}
        </p>
      )}
    </div>
  );
}
