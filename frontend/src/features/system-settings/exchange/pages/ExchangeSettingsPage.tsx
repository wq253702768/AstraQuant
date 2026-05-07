import { ApiOutlined, CheckCircleOutlined, FieldTimeOutlined, LineChartOutlined } from '@ant-design/icons';
import { Button, Descriptions, Space, Table, Tag, message } from 'antd';
import { useEffect, useState } from 'react';

import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { exchangeApi } from '@/services/exchange.api';
import type { ExchangeInstrument, ExchangeTicker, FundingRate, MarkPrice } from '@/types/exchange';

const symbols = ['BTC-USDT-SWAP', 'ETH-USDT-SWAP'];

export function ExchangeSettingsPage() {
  const [health, setHealth] = useState<string>('加载中');
  const [serverTime, setServerTime] = useState<number | null>(null);
  const [instruments, setInstruments] = useState<ExchangeInstrument[]>([]);
  const [tickers, setTickers] = useState<Record<string, ExchangeTicker>>({});
  const [marks, setMarks] = useState<Record<string, MarkPrice>>({});
  const [funding, setFunding] = useState<Record<string, FundingRate>>({});
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [healthResult, timeResult, instrumentResult] = await Promise.all([
        exchangeApi.health(),
        exchangeApi.time(),
        exchangeApi.instruments(),
      ]);
      setHealth(healthResult.status || 'ok');
      setServerTime(timeResult.server_time);
      setInstruments(instrumentResult.items.filter((item) => symbols.includes(item.internal_symbol)));
      const tickerEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.ticker(symbol)] as const));
      const markEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.markPrice(symbol)] as const));
      const fundingEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.fundingRate(symbol)] as const));
      setTickers(Object.fromEntries(tickerEntries));
      setMarks(Object.fromEntries(markEntries));
      setFunding(Object.fromEntries(fundingEntries));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '交易所公共数据加载失败';
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  return (
    <PageContainer
      title="交易所配置"
      description="查看 OKX 公共 REST 访问状态、合约规格、行情快照、标记价格与资金费率。"
      extra={<Button type="primary" loading={loading} onClick={() => void load()}>刷新公共数据</Button>}
    >
      <div className="metric-grid">
        <MetricCard title="Exchange Gateway" value={health} icon={<ApiOutlined />} tone={health === 'ok' ? 'success' : 'warning'} />
        <MetricCard title="默认交易所" value="OKX" />
        <MetricCard title="服务器时间" value={serverTime ? new Date(serverTime).toLocaleTimeString() : '-'} icon={<FieldTimeOutlined />} />
        <MetricCard title="支持品种" value={instruments.length} trend="BTC / ETH SWAP" />
      </div>

      <div className="two-column">
        <SectionCard title="BTC / ETH 合约规格" extra={<Button onClick={() => void load()}>手动刷新</Button>}>
          <Table
            rowKey="internal_symbol"
            size="small"
            pagination={false}
            loading={loading}
            dataSource={instruments}
            columns={[
              { title: '内部品种', dataIndex: 'internal_symbol' },
              { title: '交易所品种', dataIndex: 'exchange_symbol' },
              { title: '类型', dataIndex: 'contract_type' },
              { title: 'Tick Size', dataIndex: 'tick_size' },
              { title: 'Lot Size', dataIndex: 'lot_size' },
              { title: '状态', dataIndex: 'status', render: (value) => <Tag color="green">{value}</Tag> },
            ]}
          />
        </SectionCard>

        <SectionCard title="OKX 公共行情快照" extra={<LineChartOutlined />}>
          <Space direction="vertical" style={{ width: '100%' }} size={12}>
            {symbols.map((symbol) => (
              <Descriptions key={symbol} bordered size="small" column={2}>
                <Descriptions.Item label="品种">{symbol}</Descriptions.Item>
                <Descriptions.Item label="最新价">{tickers[symbol]?.last_price || '-'}</Descriptions.Item>
                <Descriptions.Item label="买一">{tickers[symbol]?.best_bid_price || '-'}</Descriptions.Item>
                <Descriptions.Item label="卖一">{tickers[symbol]?.best_ask_price || '-'}</Descriptions.Item>
                <Descriptions.Item label="标记价">{marks[symbol]?.mark_price || '-'}</Descriptions.Item>
                <Descriptions.Item label="资金费率">{funding[symbol]?.funding_rate || '-'}</Descriptions.Item>
              </Descriptions>
            ))}
          </Space>
          <div className="notice">
            <CheckCircleOutlined /> 当前数据来自 Exchange Access Gateway 公共 REST 查询，未写入历史行情库。
          </div>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
