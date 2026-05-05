import { Tag } from 'antd';
import type { ReactNode } from 'react';

const colorMap: Record<string, string> = {
  success: 'success',
  processing: 'processing',
  warning: 'warning',
  error: 'error',
  default: 'default',
  ai: 'purple',
};

interface StatusTagProps {
  status: keyof typeof colorMap | string;
  children?: ReactNode;
  text?: ReactNode;
}

export function StatusTag({ status, children, text }: StatusTagProps) {
  return <Tag color={colorMap[status] ?? status}>{children ?? text ?? status}</Tag>;
}
