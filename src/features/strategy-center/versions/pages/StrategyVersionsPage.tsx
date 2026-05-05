import { Button, Space, Table, Tabs } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';
import { StatusTag } from '@/components/status/StatusTag';
import { mockVersions } from '../../services/mockData';
import type { StrategyVersion } from '../../types';
import styles from './StrategyVersionsPage.module.css';

const columns: ColumnsType<StrategyVersion> = [
  {
    title: '版本号',
    dataIndex: 'version',
    render: (version, record) => (
      <Space>
        <span>{version}</span>
        {record.isCurrent ? <StatusTag status="success" text="当前版本" /> : null}
      </Space>
    ),
  },
  { title: '创建时间', dataIndex: 'createdAt' },
  { title: '创建人', dataIndex: 'createdBy' },
  { title: 'Code Hash', dataIndex: 'codeHash' },
  { title: '参数摘要', dataIndex: 'paramsSummary' },
  { title: '状态', dataIndex: 'status', render: value => <StatusTag status={value === '已回测' ? 'success' : value === '待回测' ? 'warning' : 'default'} text={value} /> },
  {
    title: '操作',
    render: () => (
      <Space>
        <Button type="link">回测</Button>
        <Button type="link">对比</Button>
        <Button type="link">更多</Button>
      </Space>
    ),
  },
];

export function StrategyVersionsPage() {
  return (
    <PageContainer
      title="策略版本"
      description="管理策略版本与变更，支持版本对比、回测复现与归档，保障策略演进可追溯。"
      extra={
        <Space>
          <Button>版本对比</Button>
          <Button type="primary">新建版本</Button>
        </Space>
      }
    >
      <div className={styles.layout}>
        <SectionCard title="版本列表">
          <Table rowKey="id" dataSource={mockVersions} columns={columns} pagination={false} />
        </SectionCard>
        <SectionCard title="版本对比">
          <Tabs
            items={[
              {
                key: 'params',
                label: '参数差异',
                children: (
                  <div className={styles.diffTable}>
                    <div>突破确认</div>
                    <div>2根K线</div>
                    <div>3根K线</div>
                    <div className={styles.changed}>变更</div>
                    <div>杠杆</div>
                    <div>12x</div>
                    <div>10x</div>
                    <div className={styles.changed}>变更</div>
                    <div>单笔亏损</div>
                    <div>1.5%</div>
                    <div>1.2%</div>
                    <div className={styles.changed}>变更</div>
                  </div>
                ),
              },
              { key: 'result', label: '回测结果对比', children: '收益、回撤、胜率和成本对比将在此展示。' },
              { key: 'trades', label: '交易明细对比', children: '交易数量、方向、滑点和事件链差异将在此展示。' },
            ]}
          />
        </SectionCard>
      </div>
    </PageContainer>
  );
}
