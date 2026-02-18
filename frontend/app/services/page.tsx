'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';
import { fetchServiceBlastRadius } from '@/lib/api';
import type { BlastRadiusResponse } from '@/types';
import BlastRadiusList from '@/components/BlastRadiusList';

export default function ServicesPage() {
  const [serviceName, setServiceName] = useState('');
  const [blastRadiusData, setBlastRadiusData] = useState<BlastRadiusResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = serviceName.trim();
    if (!trimmed) return;
    setLoading(true);
    setError(null);
    setBlastRadiusData(null);
    try {
      const data = await fetchServiceBlastRadius(trimmed);
      setBlastRadiusData(data);
    } catch {
      setError(`Failed to fetch blast radius for "${trimmed}". Ensure the backend is running at http://localhost:8000`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white">Services</h1>
        <p className="mt-1 text-slate-400">
          Enter a service name to view its blast radius
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={serviceName}
            onChange={(e) => setServiceName(e.target.value)}
            placeholder="e.g. auth-service, payment-gateway"
            className="w-full rounded-xl border border-slate-700 bg-slate-900/50 py-3 pl-12 pr-4 text-white placeholder-slate-500 outline-none transition-all focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !serviceName.trim()}
          className="rounded-xl bg-indigo-600 px-6 py-3 font-medium text-white transition-all hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Fetch
            </span>
          ) : (
            'Fetch Blast Radius'
          )}
        </button>
      </form>

      {error && (
        <div className="rounded-xl border border-red-500/50 bg-red-500/10 p-4 text-red-400">
          {error}
        </div>
      )}

      {blastRadiusData && (
        <div className="animate-fade-in">
          <BlastRadiusList initialData={blastRadiusData} />
        </div>
      )}
    </div>
  );
}
