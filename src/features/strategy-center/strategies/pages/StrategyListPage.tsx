import { Button, Input, Select, Space, Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { useNavigate } from 'react-router-dom';
import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { StatusTag } from '@/components/status/StatusTag';
import { routePaths } from '@/app/router/routePaths';
import { mockStrategies } from '../../services/mockData';
import type { Strategy } from '../../types';

const columns: ColumnsType<Strategy> = [
  {
    title: '策略名称',
    dataIndex: 'name',
    render: (name, record) => (
      <Space direction="vertical" size={2}>
        <strong>{name}</strong>
        <span style={{ color: '#7f8ea3' }}>{record.type}</span>
      </Space>
    ),
  },
  { title: '当前版本', dataIndex: 'currentVersion' },
  { title: '交易品种', dataIndex: 'instId' },
  { title: '周期', dataIndex: 'timeframe' },
  { title: '杠杆', dataIndex: 'leverage', render: (value) => `${value}x` },
  {
    title: '收益率',
    dataIndex: 'totalReturn',
    render: (value) => <span className="is-positive">+{value}%</span>,
  },
  {
    title: '最大回撤',
    dataIndex: 'maxDrawdown',
    render: (value) => <span className="is-negative">{value}%</span>,
  },
  { title: '胜率', dataIndex: 'winRate', render: (value) => `${value}%` },
  { title: '评分', dataIndex: 'score' },
  {
    title: '状态',
    dataIndex: 'status',
    render: (status) => <StatusTag status={status} />,
  },
];

export function StrategyListPage() {
  const navigate = useNavigate();

  return (
    <div className="page-stack">
      <div className="page-toolbar">
        <div>
          <h1>策略列表</h1>
          <p>统一管理策略状态、回测表现、风险水平与模拟盘准入。</p>
        </div>
        <Space>
          <Button>批量回测</Button>
          <Button type="primary">新建策略</Button>
        </Space>
      </div>

      <div className="metric-grid six">
        <MetricCard title="策略总数" value="18" description="当前策略池" />
        <MetricCard title="已回测" value="12" description="完成验证策略" />
        <MetricCard title="可进入模拟盘" value="5" trend="positive" description="满足准入条件" />
        <MetricCard title="高风险策略" value="3" trend="negative" description="需优先复盘" />
        <MetricCard title="平均最大回撤" value="-14.8%" trend="negative" />
        <MetricCard title="平均评分" value="76.2" description="策略池健康度" />
      </div>

      <SectionCard
        title="策略池"
        extra={
          <Space wrap>
            <Input.Search placeholder="搜索策略名 / 标签 / 合约" style={{ width: 240 }} />
            <Select placeholder="策略类型" style={{ width: 140 }} options={[{ value: 'trend', label: '趋势突破' }]} />
            <Select placeholder="状态" style={{ width: 140 }} options={[{ value: 'paper_allowed', label: '允许模拟盘' }]} />
            <Select placeholder="风险等级" style={{ width: 140 }} options={[{ value: 'medium', label: '中风险' }]} />
          </Space>
        }
      >
        <Table
          rowKey="id"
          columns={[
            ...columns,
            {
              title: '操作',
              key: 'action',
              render: (_, record) => (
                <Space>
                  <Button
                    type="link"
                    onClick={() => navigate(routePaths.strategyCenter.strategyDetail.replace(':strategyId', record.id))}
                  >
                    查看
                  </Button>
                  <Button
                    type="link"
                    onClick={() => navigate(routePaths.strategyCenter.strategyConfig.replace(':strategyId', record.id))}
                  >
                    配置
                  </Button>
                  <Button type="link" onClick={() => navigate(routePaths.strategyCenter.newBacktest)}>
                    回测
                  </Button>
                </Space>
              ),
            },
          ]}
          dataSource={mockStrategies}
          pagination={false}
        />
      </SectionCard>
    </div>
  );
}
