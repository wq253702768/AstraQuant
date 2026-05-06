import { Table, Tag } from 'antd';

import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';
import { MetricCard } from '@/components/data-display/MetricCard';

const logs = [
  {
    time: '2024-06-05 15:32:08',
    actor: '张三',
    module: 'AI策略复盘',
    event: 'AI_REVIEW_CREATED',
    target: 'BTC 趋势突破策略 v1.3.2',
    result: '成功',
    risk: '低',
    auditId: 'rev_20240605_153208',
  },
  {
    time: '2024-06-05 15:11:42',
    actor: '李四',
    module: '策略版本',
    event: 'VERSION_CREATED',
    target: 'ETH 均值回归 v3.2.0',
    result: '成功',
    risk: '中',
    auditId: 'ver_20240605_151142',
  },
  {
    time: '2024-06-05 14:42:16',
    actor: '系统',
    module: '数据校验',
    event: 'VALIDATION_FAILED',
    target: 'BT-20240605-001',
    result: '警告',
    risk: '高',
    auditId: 'val_20240605_144216',
  },
];

export function AuditLogsPage() {
  return (
    <PageContainer
      title="审计日志"
      description="追踪用户操作、策略变更、AI调用、回测执行与系统设置变更。"
    >
      <div className="metric-grid five">
        <MetricCard title="今日操作数" value="286" />
        <MetricCard title="AI调用" value="42" accent="purple" />
        <MetricCard title="策略版本变更" value="7" accent="green" />
        <MetricCard title="风险拦截事件" value="13" accent="orange" />
        <MetricCard title="异常操作" value="2" accent="red" />
      </div>

      <SectionCard title="日志列表">
        <Table
          rowKey="auditId"
          dataSource={logs}
          pagination={false}
          columns={[
            { title: '时间', dataIndex: 'time' },
            { title: '操作人', dataIndex: 'actor' },
            { title: '模块', dataIndex: 'module' },
            { title: '事件类型', dataIndex: 'event' },
            { title: '对象', dataIndex: 'target' },
            {
              title: '结果',
              dataIndex: 'result',
              render: (value) => <Tag color={value === '成功' ? 'green' : 'orange'}>{value}</Tag>,
            },
            {
              title: '风险级别',
              dataIndex: 'risk',
              render: (value) => (
                <Tag color={value === '高' ? 'red' : value === '中' ? 'orange' : 'green'}>{value}</Tag>
              ),
            },
            { title: '审计ID', dataIndex: 'auditId' },
          ]}
        />
      </SectionCard>
    </PageContainer>
  );
}
