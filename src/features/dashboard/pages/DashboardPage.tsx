import {
  ApiOutlined,
  BarChartOutlined,
  LineChartOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons';
import { Col, Row, Table, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';

import { SimpleLineChart } from '@/components/charts/SimpleLineChart';
import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';

const strategyRows = [
  {
    key: '1',
    name: 'ETH 均值回归 v3',
    status: '运行中',
    pnl: '+582.37 USDT',
    risk: '中等',
  },
  {
    key: '2',
    name: 'BTC 趋势突破策略',
    status: '待回测',
    pnl: '-',
    risk: '低',
  },
  {
    key: '3',
    name: 'ETH 网格震荡策略',
    status: '待优化',
    pnl: '-214.62 USDT',
    risk: '高',
  },
];

const columns: ColumnsType<(typeof strategyRows)[number]> = [
  { title: '策略名称', dataIndex: 'name' },
  {
    title: '状态',
    dataIndex: 'status',
    render: (value) => <Tag color={value === '运行中' ? 'green' : value === '待优化' ? 'gold' : 'blue'}>{value}</Tag>,
  },
  { title: '今日盈亏', dataIndex: 'pnl' },
  {
    title: '风险',
    dataIndex: 'risk',
    render: (value) => <Tag color={value === '高' ? 'red' : value === '中等' ? 'gold' : 'green'}>{value}</Tag>,
  },
];

export function DashboardPage() {
  return (
    <PageContainer
      title="总览大盘"
      description="集中查看资产概览、策略运行、回测任务、风险状态与系统连接。"
    >
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <MetricCard title="策略总数" value="18" trend="+3 本月" icon={<LineChartOutlined />} />
        </Col>
        <Col span={6}>
          <MetricCard title="可进入模拟盘" value="5" trend="准入率 27.8%" tone="success" icon={<SafetyCertificateOutlined />} />
        </Col>
        <Col span={6}>
          <MetricCard title="AI复盘任务" value="42" trend="今日调用" tone="ai" icon={<RobotOutlined />} />
        </Col>
        <Col span={6}>
          <MetricCard title="系统连接" value="正常" trend="OKX / AI / 审计" tone="success" icon={<ApiOutlined />} />
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col span={16}>
          <SectionCard title="策略池净值概览" extra="近90天">
            <SimpleLineChart height={280} color="#1677ff" />
          </SectionCard>
        </Col>
        <Col span={8}>
          <SectionCard title="风险概览">
            <MetricCard title="平均最大回撤" value="-14.8%" tone="danger" />
            <div style={{ height: 12 }} />
            <MetricCard title="平均评分" value="76.2" tone="success" />
          </SectionCard>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col span={14}>
          <SectionCard title="策略运行状态">
            <Table columns={columns} dataSource={strategyRows} pagination={false} />
          </SectionCard>
        </Col>
        <Col span={10}>
          <SectionCard title="近期任务">
            <MetricCard title="回测执行中" value="3" trend="Worker 12/16" icon={<BarChartOutlined />} />
            <div style={{ height: 12 }} />
            <MetricCard title="待处理审计" value="2" tone="warning" trend="高风险操作需复核" />
          </SectionCard>
        </Col>
      </Row>
    </PageContainer>
  );
}
