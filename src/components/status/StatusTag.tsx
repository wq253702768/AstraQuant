import { Tag } from 'antd';
import type { ReactNode } from 'react';

const colorMap: Record<string, string> = {
  success: 'success',
  processing: 'processing',
  warning: 'warning',
  error: 'error',
  default: 'default',
  ai: 'purple',
  allowed_paper: 'success',
  paper_allowed: 'success',
  optimize: 'warning',
  optimizing: 'warning',
  high_risk: 'error',
  pending_backtest: 'processing',
  pending: 'processing',
  backtested: 'success',
  archived: 'default',
  paper_trading: 'success',
};

const textMap: Record<string, ReactNode> = {
  allowed_paper: '允许模拟盘',
  paper_allowed: '允许模拟盘',
  optimize: '待优化',
  optimizing: '待优化',
  high_risk: '高风险',
  pending_backtest: '待回测',
  pending: '待回测',
  backtested: '已回测',
  archived: '已归档',
  paper_trading: '模拟盘',
};

interface StatusTagProps {
  status: keyof typeof colorMap | string;
  children?: ReactNode;
  text?: ReactNode;
}

export function StatusTag({ status, children, text }: StatusTagProps) {
  return <Tag color={colorMap[status] ?? status}>{children ?? text ?? textMap[status] ?? status}</Tag>;
}
