import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  RiskScore,
  MetricsResponse,
  BlastRadiusResponse,
  Deployment,
} from '@/types';

const BASE_URL = 'http://localhost:8000';

const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Response handlers
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 404 || error.code === 'ECONNREFUSED') {
      console.warn('Backend not available, using fallback data');
    }
    return Promise.reject(error);
  }
);

// Risk Score API
export async function fetchLatestRiskScore(): Promise<RiskScore | null> {
  try {
    const { data } = await api.get<RiskScore>('/risk-score/latest');
    return data;
  } catch {
    // Fallback for when backend is unavailable
    return {
      score: 42,
      decision: 'manual_review',
      timestamp: new Date().toISOString(),
    };
  }
}

// Metrics API
export async function fetchMetrics(): Promise<MetricsResponse> {
  try {
    const { data } = await api.get<MetricsResponse>('/metrics');
    return data;
  } catch {
    // Generate fallback metrics data
    const now = Date.now();
    const data = Array.from({ length: 12 }, (_, i) => ({
      timestamp: new Date(now - (11 - i) * 60000).toISOString(),
      latency: 80 + Math.random() * 120,
      error_rate: Math.random() * 2,
      cpu: 40 + Math.random() * 40,
      memory: 50 + Math.random() * 30,
    }));
    return { data };
  }
}

// Service Blast Radius API
export async function fetchServiceBlastRadius(
  service: string
): Promise<BlastRadiusResponse> {
  try {
    const { data } = await api.get<BlastRadiusResponse>(
      `/service-blast-radius/${encodeURIComponent(service)}`
    );
    return data;
  } catch {
    throw new Error(`Failed to fetch blast radius for ${service}`);
  }
}

// Deployments (mock - backend may not have this endpoint)
export async function fetchDeployments(): Promise<Deployment[]> {
  try {
    const { data } = await api.get<Deployment[]>('/deployments');
    return Array.isArray(data) ? data : [];
  } catch {
    // Mock fallback data
    const now = new Date();
    return [
      {
        id: 'dep-001',
        service_name: 'auth-service',
        risk_score: 25,
        decision: 'approve',
        timestamp: new Date(now.getTime() - 3600000).toISOString(),
        status: 'success',
      },
      {
        id: 'dep-002',
        service_name: 'payment-gateway',
        risk_score: 72,
        decision: 'reject',
        timestamp: new Date(now.getTime() - 7200000).toISOString(),
        status: 'failed',
      },
      {
        id: 'dep-003',
        service_name: 'user-profile-api',
        risk_score: 45,
        decision: 'manual_review',
        timestamp: new Date(now.getTime() - 10800000).toISOString(),
        status: 'pending',
      },
      {
        id: 'dep-004',
        service_name: 'notification-service',
        risk_score: 18,
        decision: 'approve',
        timestamp: new Date(now.getTime() - 14400000).toISOString(),
        status: 'success',
      },
      {
        id: 'dep-005',
        service_name: 'search-indexer',
        risk_score: 55,
        decision: 'manual_review',
        timestamp: new Date(now.getTime() - 18000000).toISOString(),
        status: 'pending',
      },
    ];
  }
}

export default api;
