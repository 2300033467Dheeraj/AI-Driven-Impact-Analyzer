'use client';

import { useEffect, useState } from 'react';
import RiskCard from '@/components/RiskCard';
import RiskGauge from '@/components/RiskGauge';
import MetricsChart from '@/components/MetricsChart';
import BlastRadiusList from '@/components/BlastRadiusList';
import DeploymentTable from '@/components/DeploymentTable';
import DecisionBadge from '@/components/DecisionBadge';
import { fetchLatestRiskScore } from '@/lib/api';
import { RefreshCw } from 'lucide-react';

const REFRESH_INTERVAL = 10000; // 10 seconds

export default function DashboardPage() {
  const [decision, setDecision] = useState<'approve' | 'reject' | 'manual_review' | null>(null);

  useEffect(() => {
    async function loadDecision() {
      const data = await fetchLatestRiskScore();
      if (data) setDecision(data.decision);
    }
    loadDecision();
  }, []);

  // Auto-refresh every 10 seconds - use key to force re-mount of child components
  const [refreshKey, setRefreshKey] = useState(0);
  useEffect(() => {
    const id = setInterval(() => {
      setRefreshKey((k) => k + 1);
      fetchLatestRiskScore().then((data) => {
        if (data) setDecision(data.decision);
      });
    }, REFRESH_INTERVAL);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="mt-1 text-slate-400">
            AI-driven risk analysis for cloud-native deployments
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <RefreshCw className="h-4 w-4 text-slate-500" />
            Auto-refresh every 10s
          </div>
          {decision && (
            <DecisionBadge decision={decision} size="lg" />
          )}
        </div>
      </div>

      {/* Risk Score + Gauge row - key forces re-fetch on auto-refresh */}
      <div key={`risk-${refreshKey}`} className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <RiskCard />
        </div>
        <div>
          <RiskGauge />
        </div>
      </div>

      {/* Metrics Chart full width */}
      <div key={`metrics-${refreshKey}`}>
        <MetricsChart />
      </div>

      {/* Blast Radius + Recent Deployments */}
      <div key={`deployments-${refreshKey}`} className="grid gap-6 lg:grid-cols-3">
        <div>
          <BlastRadiusList />
        </div>
        <div className="lg:col-span-2">
          <DeploymentTable />
        </div>
      </div>
    </div>
  );
}
