'use client';

import DeploymentTable from '@/components/DeploymentTable';

export default function DeploymentsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white">Deployments</h1>
        <p className="mt-1 text-slate-400">
          View past deployments with risk scores and decisions
        </p>
      </div>

      <DeploymentTable />
    </div>
  );
}
