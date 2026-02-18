'use client';

import { useEffect, useState } from 'react';
import { fetchDeployments } from '@/lib/api';
import type { Deployment } from '@/types';
import DecisionBadge from './DecisionBadge';
import { CheckCircle2, XCircle, Clock } from 'lucide-react';

function getStatusIcon(status?: string) {
  switch (status) {
    case 'success':
      return <CheckCircle2 className="h-4 w-4 text-emerald-400" />;
    case 'failed':
      return <XCircle className="h-4 w-4 text-red-400" />;
    default:
      return <Clock className="h-4 w-4 text-amber-400" />;
  }
}

function getRiskColor(score: number): string {
  if (score <= 30) return 'text-emerald-400';
  if (score <= 60) return 'text-amber-400';
  return 'text-red-400';
}

export default function DeploymentTable() {
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchDeployments();
        setDeployments(data);
      } catch {
        setDeployments([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-8 shadow-xl backdrop-blur">
        <div className="flex items-center justify-center py-24">
          <div className="h-12 w-12 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 shadow-xl backdrop-blur overflow-hidden">
      <div className="border-b border-slate-800 px-6 py-4">
        <h2 className="text-lg font-semibold text-white">Deployments</h2>
        <p className="text-sm text-slate-400">Recent deployment history</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900/50">
              <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                Status
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                Service
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                Risk Score
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                Decision
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                Timestamp
              </th>
            </tr>
          </thead>
          <tbody>
            {deployments.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-slate-500">
                  No deployments found
                </td>
              </tr>
            ) : (
              deployments.map((dep) => (
                <tr
                  key={dep.id}
                  className="border-b border-slate-800/50 transition-colors hover:bg-slate-800/30"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(dep.status)}
                      <span className="text-sm text-slate-400 capitalize">
                        {dep.status ?? 'pending'}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-mono text-sm text-slate-200">
                    {dep.service_name}
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`font-semibold tabular-nums ${getRiskColor(dep.risk_score)}`}
                    >
                      {dep.risk_score}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <DecisionBadge decision={dep.decision} size="sm" />
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">
                    {new Date(dep.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
