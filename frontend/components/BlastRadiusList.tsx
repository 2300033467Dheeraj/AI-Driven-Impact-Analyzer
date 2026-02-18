'use client';

import { useEffect, useState } from 'react';
import { fetchLatestRiskScore, fetchServiceBlastRadius } from '@/lib/api';
import type { BlastRadiusResponse } from '@/types';
import { Server } from 'lucide-react';

// Default blast radius for dashboard when no service-specific data
const DEFAULT_IMPACTED = ['auth-service', 'payment-gateway', 'user-profile-api'];

interface BlastRadiusListProps {
  serviceName?: string;
  /** Pre-fetched data; when provided, skips fetch */
  initialData?: BlastRadiusResponse;
}

export default function BlastRadiusList({ serviceName, initialData }: BlastRadiusListProps) {
  const [impactedServices, setImpactedServices] = useState<string[]>(
    initialData?.impacted_services ?? []
  );
  const [sourceService, setSourceService] = useState<string | null>(
    initialData?.service ?? null
  );
  const [loading, setLoading] = useState(!initialData);

  useEffect(() => {
    if (initialData) {
      setImpactedServices(initialData.impacted_services ?? []);
      setSourceService(initialData.service);
      setLoading(false);
      return;
    }

    async function load() {
      setLoading(true);
      try {
        if (serviceName?.trim()) {
          const data = await fetchServiceBlastRadius(serviceName.trim());
          setImpactedServices(data.impacted_services ?? []);
          setSourceService(data.service);
        } else {
          try {
            await fetchLatestRiskScore();
            setImpactedServices(DEFAULT_IMPACTED);
            setSourceService('system');
          } catch {
            setImpactedServices(DEFAULT_IMPACTED);
            setSourceService('system');
          }
        }
      } catch {
        setImpactedServices(DEFAULT_IMPACTED);
        setSourceService(null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [serviceName, initialData]);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur">
        <div className="flex h-48 items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur transition-all hover:border-slate-700">
      <div className="mb-4 flex items-center gap-2">
        <Server className="h-5 w-5 text-slate-400" />
        <h3 className="text-sm font-medium uppercase tracking-wider text-slate-400">
          Blast Radius
          {sourceService && sourceService !== 'system' && (
            <span className="ml-2 text-slate-500">for {sourceService}</span>
          )}
        </h3>
      </div>
      {impactedServices.length === 0 ? (
        <p className="text-sm text-slate-500">No impacted services</p>
      ) : (
        <ul className="space-y-2">
          {impactedServices.map((svc, i) => (
            <li
              key={`${svc}-${i}`}
              className="flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-800/30 px-4 py-2.5 transition-all hover:border-slate-700 hover:bg-slate-800/50"
            >
              <span className="h-2 w-2 rounded-full bg-amber-500" />
              <span className="font-mono text-sm text-slate-200">{svc}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
