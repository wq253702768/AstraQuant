import {
  backtestMetrics,
  costMetrics,
  lineData,
  strategies,
  trades,
  versions,
} from '../data/strategyData.js';
import type { Strategy, StrategyStatus } from '../types.js';

interface StrategyFilters {
  status?: string;
  riskLevel?: string;
  keyword?: string;
}

export function listStrategies(filters: StrategyFilters = {}) {
  return strategies.filter((strategy) => {
    const matchesStatus = !filters.status || normalizeStatus(strategy.status) === normalizeStatus(filters.status);
    const matchesRisk = !filters.riskLevel || strategy.riskLevel === filters.riskLevel;
    const keyword = filters.keyword?.trim().toLowerCase();
    const matchesKeyword =
      !keyword ||
      [strategy.name, strategy.type, strategy.instId, strategy.currentVersion].some((value) =>
        value.toLowerCase().includes(keyword),
      );

    return matchesStatus && matchesRisk && matchesKeyword;
  });
}

export function getStrategy(strategyId: string) {
  return strategies.find((strategy) => strategy.id === strategyId);
}

export function getStrategyVersions(strategyId: string) {
  const strategy = getStrategy(strategyId);

  if (!strategy) {
    return null;
  }

  return versions.map((version) => ({
    ...version,
    strategyId,
  }));
}

export function getBacktestMetrics(taskId: string) {
  return {
    taskId,
    items: backtestMetrics,
    equityCurve: lineData.map((value, index) => ({
      index,
      value,
    })),
  };
}

export function getStrategyTrades(taskId: string, filters: { instId?: string } = {}) {
  const filteredTrades = filters.instId ? trades.filter((trade) => trade.instId === filters.instId) : trades;

  return {
    taskId,
    items: filteredTrades,
    total: filteredTrades.length,
  };
}

export function getCostMetrics(taskId: string) {
  return {
    taskId,
    items: costMetrics,
  };
}

export function getDashboardOverview() {
  const strategyTotal = strategies.length;
  const paperAllowed = strategies.filter((strategy) => normalizeStatus(strategy.status) === 'allowed_paper').length;
  const averageScore = average(strategies.map((strategy) => strategy.score));
  const averageDrawdown = average(strategies.map((strategy) => strategy.maxDrawdown));

  return {
    metrics: {
      strategyTotal,
      paperAllowed,
      paperAllowedRate: strategyTotal > 0 ? round((paperAllowed / strategyTotal) * 100) : 0,
      aiReviewTasksToday: 42,
      systemStatus: 'normal',
      averageScore,
      averageDrawdown,
    },
    strategyRows: strategies.map(toDashboardStrategyRow),
    recentTasks: [
      { id: 'bt-running', title: '回测执行中', value: 3, detail: 'Worker 12/16' },
      { id: 'audit-pending', title: '待处理审计', value: 2, detail: '高风险操作需复核' },
    ],
  };
}

function toDashboardStrategyRow(strategy: Strategy) {
  return {
    id: strategy.id,
    name: strategy.name,
    status: toDashboardStatus(strategy.status),
    pnl: strategy.totalReturn >= 0 ? `+${strategy.totalReturn}%` : `${strategy.totalReturn}%`,
    risk: strategy.riskLevel ?? 'low',
  };
}

function toDashboardStatus(status: StrategyStatus | 'allowed_paper' | 'optimize') {
  switch (normalizeStatus(status)) {
    case 'allowed_paper':
    case 'paper_allowed':
      return '运行中';
    case 'optimize':
    case 'optimizing':
      return '待优化';
    case 'high_risk':
      return '高风险';
    case 'pending_backtest':
    default:
      return '待回测';
  }
}

function normalizeStatus(status: string) {
  if (status === 'paper_allowed') {
    return 'allowed_paper';
  }

  if (status === 'optimizing') {
    return 'optimize';
  }

  return status;
}

function average(values: number[]) {
  if (values.length === 0) {
    return 0;
  }

  return round(values.reduce((sum, value) => sum + value, 0) / values.length);
}

function round(value: number) {
  return Math.round(value * 100) / 100;
}
