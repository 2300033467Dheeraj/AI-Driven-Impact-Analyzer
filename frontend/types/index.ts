// Risk Score Types
export interface RiskScore {
  score: number;
  decision: 'approve' | 'reject' | 'manual_review';
  timestamp?: string;
  deployment_id?: string;
}

// Metrics Types
export interface MetricDataPoint {
  timestamp: string;
  latency?: number;
  error_rate?: number;
  cpu?: number;
  memory?: number;
}

export interface MetricsResponse {
  data: MetricDataPoint[];
  period?: string;
}

// Blast Radius Types
export interface BlastRadiusResponse {
  service: string;
  impacted_services: string[];
}

// Deployment Types
export interface Deployment {
  id: string;
  service_name: string;
  risk_score: number;
  decision: 'approve' | 'reject' | 'manual_review';
  timestamp: string;
  status?: 'success' | 'failed' | 'pending';
}
