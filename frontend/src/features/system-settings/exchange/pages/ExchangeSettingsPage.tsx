import { ApiOutlined, CheckCircleOutlined, FieldTimeOutlined, LineChartOutlined } from '@ant-design/icons';
import { Button, Descriptions, Select, Space, Table, Tag, message } from 'antd';
import { useEffect, useState } from 'react';

import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { exchangeApi } from '@/services/exchange.api';
import type { ExchangeInstrument, ExchangeTicker, FundingRate, MarkPrice, OpenInterest } from '@/types/exchange';

const symbols = ['BTC-USDT-SWAP', 'ETH-USDT-SWAP'];

export function ExchangeSettingsPage() {
  const [health, setHealth] = useState<string>('加载中');
  const [serverTime, setServerTime] = useState<number | null>(null);
  const [instruments, setInstruments] = useState<ExchangeInstrument[]>([]);
  const [storedInstruments, setStoredInstruments] = useState<ExchangeInstrument[]>([]);
  const [mappings, setMappings] = useState<Array<{ internal_symbol: string; exchange: string; exchange_symbol: string; inst_type: string; enabled: boolean }>>([]);
  const [tickers, setTickers] = useState<Record<string, ExchangeTicker>>({});
  const [marks, setMarks] = useState<Record<string, MarkPrice>>({});
  const [funding, setFunding] = useState<Record<string, FundingRate>>({});
  const [openInterest, setOpenInterest] = useState<Record<string, OpenInterest>>({});
  const [klines, setKlines] = useState<Array<Record<string, unknown>>>([]);
  const [fundingHistory, setFundingHistory] = useState<FundingRate[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState('BTC-USDT-SWAP');
  const [timeframe, setTimeframe] = useState('5m');
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [healthResult, timeResult, instrumentResult, storedResult, mappingResult] = await Promise.all([
        exchangeApi.health(),
        exchangeApi.time(),
        exchangeApi.instruments(),
        exchangeApi.storedInstruments(),
        exchangeApi.symbolMappings(),
      ]);
      setHealth(healthResult.status || 'ok');
      setServerTime(timeResult.server_time);
      setInstruments(instrumentResult.items.filter((item) => symbols.includes(item.internal_symbol)));
      setStoredInstruments(storedResult.items || []);
      setMappings(mappingResult.items || []);
      const tickerEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.ticker(symbol)] as const));
      const markEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.markPrice(symbol)] as const));
      const fundingEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.fundingRate(symbol)] as const));
      const openInterestEntries = await Promise.all(symbols.map(async (symbol) => [symbol, await exchangeApi.openInterest(symbol)] as const));
      setTickers(Object.fromEntries(tickerEntries));
      setMarks(Object.fromEntries(markEntries));
      setFunding(Object.fromEntries(fundingEntries));
      setOpenInterest(Object.fromEntries(openInterestEntries));
      await loadSeries(selectedSymbol, timeframe);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '交易所公共数据加载失败';
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const loadSeries = async (symbol = selectedSymbol, tf = timeframe) => {
    const [klineResult, fundingResult] = await Promise.all([
      exchangeApi.klines(symbol, tf, 5),
      exchangeApi.fundingRateHistory(symbol, 5),
    ]);
    setKlines(klineResult.items);
    setFundingHistory(fundingResult.items);
  };

  const sync = async () => {
    const result = await exchangeApi.syncInstruments();
    message.success(`同步完成：${result.success_count} 个合约`);
    await load();
  };

  useEffect(() => {
    void load();
  }, []);

  return (
    <PageContainer title="交易所配置" description="查看 OKX 公共 REST 访问状态、合约规格、行情快照、标记价格与资金费率。" extra={<Button type="primary" loading={loading} onClick={() => void load()}>刷新公共数据</Button>}>
      <div className="metric-grid">
        <MetricCard title="Exchange Gateway" value={health} icon={<ApiOutlined />} tone={health === 'ok' ? 'success' : 'warning'} />
        <MetricCard title="默认交易所" value="OKX" />
        <MetricCard title="服务器时间" value={serverTime ? new Date(serverTime).toLocaleTimeString() : '-'} icon={<FieldTimeOutlined />} />
        <MetricCard title="已同步合约" value={storedInstruments.length} trend="BTC / ETH SWAP" />
      </div>

      <div className="two-column">
        <SectionCard title="已同步合约规格" extra={<Button onClick={() => void sync()}>手动同步合约</Button>}>
          <Table rowKey="internal_symbol" size="small" pagination={false} loading={loading} dataSource={storedInstruments.length ? storedInstruments : instruments} columns={[
            { title: '内部品种', dataIndex: 'internal_symbol' },
            { title: '交易所品种', dataIndex: 'exchange_symbol' },
            { title: '类型', dataIndex: 'contract_type' },
            { title: 'Tick Size', dataIndex: 'tick_size' },
            { title: 'Lot Size', dataIndex: 'lot_size' },
            { title: 'Contract Value', dataIndex: 'contract_value' },
            { title: '状态', dataIndex: 'status', render: (value) => <Tag color="green">{value}</Tag> },
          ]} />
        </SectionCard>

        <SectionCard title="Symbol 映射">
          <Table rowKey="internal_symbol" size="small" pagination={false} dataSource={mappings} columns={[
            { title: 'Internal', dataIndex: 'internal_symbol' },
            { title: 'Exchange', dataIndex: 'exchange' },
            { title: 'Exchange Symbol', dataIndex: 'exchange_symbol' },
            { title: '类型', dataIndex: 'inst_type' },
            { title: '启用', dataIndex: 'enabled', render: (value) => <Tag color={value ? 'green' : 'default'}>{String(value)}</Tag> },
          ]} />
        </SectionCard>
      </div>

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
                <Descriptions.Item label="持仓量">{openInterest[symbol]?.open_interest || '-'}</Descriptions.Item>
                <Descriptions.Item label="持仓币量">{openInterest[symbol]?.open_interest_ccy || '-'}</Descriptions.Item>
            </Descriptions>
          ))}
        </Space>
      </SectionCard>

      <div className="two-column">
        <SectionCard title="K线查询" extra={<Space><Select value={selectedSymbol} options={symbols.map((value) => ({ value }))} onChange={setSelectedSymbol} /><Select value={timeframe} options={['1m', '5m', '15m', '1h', '4h'].map((value) => ({ value }))} onChange={setTimeframe} /><Button onClick={() => void loadSeries()}>查询</Button></Space>}>
          <Table rowKey={(row) => String(row.timestamp)} size="small" pagination={false} dataSource={klines} columns={[
            { title: '时间', dataIndex: 'timestamp', render: (value) => new Date(Number(value)).toLocaleString() },
            { title: 'Open', dataIndex: 'open' },
            { title: 'High', dataIndex: 'high' },
            { title: 'Low', dataIndex: 'low' },
            { title: 'Close', dataIndex: 'close' },
            { title: 'Volume', dataIndex: 'volume' },
          ]} />
        </SectionCard>
        <SectionCard title="资金费率历史">
          <Table rowKey={(row) => `${row.internal_symbol}-${row.funding_time}`} size="small" pagination={false} dataSource={fundingHistory} columns={[
            { title: '品种', dataIndex: 'internal_symbol' },
            { title: '资金费率', dataIndex: 'funding_rate' },
            { title: '时间', dataIndex: 'funding_time', render: (value) => new Date(Number(value)).toLocaleString() },
          ]} />
          <div className="notice"><CheckCircleOutlined /> 当前数据来自 Exchange Access Gateway 公共 REST 查询，未写入历史行情库。</div>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
