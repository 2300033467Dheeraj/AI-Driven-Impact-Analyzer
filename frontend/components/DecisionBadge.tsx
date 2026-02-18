'use client';

import { CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import type { RiskScore } from '@/types';

type Decision = RiskScore['decision'];

interface DecisionBadgeProps {
  decision: Decision;
  size?: 'sm' | 'md' | 'lg';
}

const config: Record<
  Decision,
  { label: string; color: string; bgColor: string; icon: typeof CheckCircle2 }
> = {
  approve: {
    label: 'Approve',
    color: 'text-emerald-400',
    bgColor: 'bg-emerald-500/20 border-emerald-500/50',
    icon: CheckCircle2,
  },
  reject: {
    label: 'Reject',
    color: 'text-red-400',
    bgColor: 'bg-red-500/20 border-red-500/50',
    icon: XCircle,
  },
  manual_review: {
    label: 'Manual Review',
    color: 'text-amber-400',
    bgColor: 'bg-amber-500/20 border-amber-500/50',
    icon: AlertCircle,
  },
};

export default function DecisionBadge({ decision, size = 'md' }: DecisionBadgeProps) {
  const { label, color, bgColor, icon: Icon } = config[decision];

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-3 py-1.5 text-sm gap-2',
    lg: 'px-4 py-2 text-base gap-2',
  };

  const iconSizes = {
    sm: 'h-3.5 w-3.5',
    md: 'h-4 w-4',
    lg: 'h-5 w-5',
  };

  return (
    <span
      className={`inline-flex items-center rounded-lg border font-medium transition-all hover:scale-[1.02] ${bgColor} ${color} ${sizeClasses[size]}`}
    >
      <Icon className={iconSizes[size]} />
      {label}
    </span>
  );
}
