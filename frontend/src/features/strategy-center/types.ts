export type StrategyStatus = 'paper_allowed' | 'optimizing' | 'high_risk' | 'pending_backtest';

export interface Strategy {
  id: string;
  name: string;
  currentVersion: string;
  version?: string;
  type: string;
  instId: string;
  timeframe: string;
  leverage: number | string;
  totalReturn: number;
  maxDrawdown: number;
  winRate: number;
  score: number;
  status: StrategyStatus | 'allowed_paper' | 'optimize';
  riskLevel?: 'low' | 'medium' | 'high';
}

export type StrategyListItem = Strategy;

export interface StrategyVersion {
  id: string;
  version: string;
  status: 'pending' | 'backtested' | 'archived' | 'paper_trading';
  codeHash: string;
  createdAt: string;
  createdBy: string;
  paramsSummary: string;
  isCurrent?: boolean;
}

export interface BacktestMetric {
  label: string;
  value: string;
  trend?: 'positive' | 'negative' | 'neutral' | 'up' | 'down';
  description?: string;
  extra?: string;
}

export interface CostMetric {
  label: string;
  value: string;
  unit: string;
  ratio: string;
}

export interface TradeRecord {
  id: string;
  time: string;
  instId: string;
  action: string;
  direction: string;
  leverage: string;
  orderType: string;
  fillPrice: number;
  fee: number;
  slippage: number;
  pnl: number;
  status: string;
}
