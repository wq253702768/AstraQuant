import { ApiOutlined, CheckCircleOutlined, SafetyOutlined } from '@ant-design/icons';
import { Button, Descriptions, Table, Tag } from 'antd';

import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';

const permissionRows = [
  { key: 'market', name: '行情权限', status: '通过' },
  { key: 'account', name: '账户读取', status: '通过' },
  { key: 'history', name: '历史K线', status: '通过' },
  { key: 'funding', name: '资金费率', status: '通过' },
  { key: 'paper', name: '模拟盘交易', status: '通过' },
  { key: 'live', name: '实盘交易', status: '关闭' },
  { key: 'withdraw', name: '提币权限', status: '禁止' },
];

export function ExchangeSettingsPage() {
  return (
    <PageContainer
      title="交易所配置"
      description="管理 OKX 行情、历史数据、模拟盘与后续实盘交易所连接。"
      extra={<Button type="primary">新增交易所</Button>}
    >
      <div className="metric-grid">
        <MetricCard title="已配置交易所" value="1" icon={<ApiOutlined />} />
        <MetricCard title="默认交易所" value="OKX" />
        <MetricCard title="OKX连接状态" value="正常" trend="positive" />
        <MetricCard title="行情数据状态" value="正常" trend="positive" />
        <MetricCard title="最近检测" value="2分钟前" />
      </div>
      <div className="two-column">
        <SectionCard title="交易所列表">
          <div className="stack">
            {['OKX', 'Binance', 'Bybit', 'Gate.io'].map((exchange, index) => (
              <div className="list-card" key={exchange}>
                <div>
                  <strong>{exchange}</strong>
                  <div className="muted">{index === 0 ? '行情 / 历史数据 / 模拟盘' : '待接入'}</div>
                </div>
                <Tag color={index === 0 ? 'green' : 'default'}>{index === 0 ? '正常' : '预留'}</Tag>
              </div>
            ))}
          </div>
        </SectionCard>
        <SectionCard
          title="OKX 配置详情"
          extra={<Button icon={<SafetyOutlined />}>连接测试</Button>}
        >
          <Descriptions column={2} size="small">
            <Descriptions.Item label="环境">模拟盘</Descriptions.Item>
            <Descriptions.Item label="权限范围">只读 + 模拟盘</Descriptions.Item>
            <Descriptions.Item label="API Key">****a9f7</Descriptions.Item>
            <Descriptions.Item label="Secret Key">已加密</Descriptions.Item>
            <Descriptions.Item label="Passphrase">已配置</Descriptions.Item>
            <Descriptions.Item label="IP白名单">已启用</Descriptions.Item>
          </Descriptions>
          <Table
            rowKey="key"
            size="small"
            pagination={false}
            dataSource={permissionRows}
            columns={[
              { title: '检测项', dataIndex: 'name' },
              {
                title: '结果',
                dataIndex: 'status',
                render: (value: string) => (
                  <Tag color={value === '通过' ? 'green' : value === '禁止' ? 'red' : 'gold'}>
                    {value}
                  </Tag>
                ),
              },
            ]}
          />
          <div className="notice">实盘交易关闭 · 提币权限禁止</div>
          <div className="notice">
            <CheckCircleOutlined /> 第一阶段建议仅启用只读和模拟盘权限，不配置提币权限。
          </div>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
