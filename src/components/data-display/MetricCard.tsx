import { ReactNode } from 'react';
import { Card, Space, Typography } from 'antd';
import clsx from 'clsx';
import styles from './MetricCard.module.css';

type MetricTone = 'default' | 'success' | 'danger' | 'warning' | 'primary' | 'purple' | 'ai';

interface MetricCardProps {
  title: string;
  value: ReactNode;
  suffix?: ReactNode;
  description?: ReactNode;
  trend?: ReactNode;
  status?: ReactNode;
  accent?: string;
  icon?: ReactNode;
  tone?: MetricTone;
}

export function MetricCard({
  title,
  value,
  suffix,
  description,
  trend,
  status,
  accent,
  icon,
  tone = 'default',
}: MetricCardProps) {
  return (
    <Card className={clsx(styles.card, styles[tone])} style={accent ? { borderColor: accent } : undefined}>
      <Space className={styles.header} align="center">
        {icon ? <span className={styles.icon}>{icon}</span> : null}
        <Typography.Text type="secondary">{title}</Typography.Text>
        {status ? <span className={styles.status}>{status}</span> : null}
      </Space>
      <div className={styles.value}>
        <span>{value}</span>
        {suffix ? <small>{suffix}</small> : null}
      </div>
      {trend ? <div className={styles.trend}>{trend}</div> : null}
      {description ? <div className={styles.description}>{description}</div> : null}
    </Card>
  );
}
