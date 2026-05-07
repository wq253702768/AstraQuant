import { Button, DatePicker, Form, Select, Space, Table, Tag, message } from 'antd';
import dayjs from 'dayjs';
import { useEffect, useState } from 'react';

import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { marketDataApi } from '@/services/market-data.api';
import type { Kline, SyncTask } from '@/types/market-data';

interface FormValues {
  symbol: string;
  timeframe: string;
  range: [dayjs.Dayjs, dayjs.Dayjs];
}

export function MarketDataPage() {
  const [form] = Form.useForm<FormValues>();
  const [health, setHealth] = useState('加载中');
  const [tasks, setTasks] = useState<SyncTask[]>([]);
  const [klines, setKlines] = useState<Kline[]>([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    const [healthResult, taskResult] = await Promise.all([marketDataApi.health(), marketDataApi.listSyncTasks()]);
    setHealth(healthResult.status || 'ok');
    setTasks(taskResult.items);
  };

  useEffect(() => {
    form.setFieldsValue({
      symbol: 'BTC-USDT-SWAP',
      timeframe: '5m',
      range: [dayjs().subtract(6, 'hour'), dayjs()],
    });
    void load();
  }, []);

  const createAndRun = async (values: FormValues) => {
    setLoading(true);
    try {
      const task = await marketDataApi.createSyncTask({
        exchange: 'OKX',
        symbols: [values.symbol],
        data_types: ['kline'],
        timeframes: [values.timeframe],
        start_time: values.range[0].toISOString(),
        end_time: values.range[1].toISOString(),
      });
      const result = await marketDataApi.runSyncTask(task.sync_task_id);
      message.success(`同步完成：inserted=${result.inserted_count} updated=${result.updated_count}`);
      await load();
      await queryKlines(values);
    } finally {
      setLoading(false);
    }
  };

  const queryKlines = async (values = form.getFieldsValue()) => {
    const result = await marketDataApi.candles({
      exchange: 'OKX',
      symbol: values.symbol,
      timeframe: values.timeframe,
      start_time: values.range?.[0]?.toISOString(),
      end_time: values.range?.[1]?.toISOString(),
      limit: 100,
    });
    setKlines(result.items);
  };

  return (
    <PageContainer title="历史行情" description="从 Exchange Access Gateway 同步 K线到本地数据库，并查询已入库数据。">
      <div className="metric-grid">
        <MetricCard title="Market Data Service" value={health} tone={health === 'ok' ? 'success' : 'warning'} />
        <MetricCard title="同步任务数" value={tasks.length} />
        <MetricCard title="当前K线数量" value={klines.length} />
        <MetricCard title="当前阶段" value="K线同步" />
      </div>

      <SectionCard title="创建并运行 K线同步任务">
        <Form form={form} layout="inline" onFinish={createAndRun}>
          <Form.Item name="symbol" label="品种">
            <Select style={{ width: 180 }} options={['BTC-USDT-SWAP', 'ETH-USDT-SWAP'].map((value) => ({ value }))} />
          </Form.Item>
          <Form.Item name="timeframe" label="周期">
            <Select style={{ width: 100 }} options={['1m', '5m', '15m', '1h', '4h'].map((value) => ({ value }))} />
          </Form.Item>
          <Form.Item name="range" label="时间范围">
            <DatePicker.RangePicker showTime />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={loading}>创建并运行</Button>
              <Button onClick={() => void queryKlines()}>查询K线</Button>
            </Space>
          </Form.Item>
        </Form>
      </SectionCard>

      <SectionCard title="同步任务">
        <Table rowKey="sync_task_id" size="small" pagination={false} dataSource={tasks.slice(0, 8)} columns={[
          { title: '任务ID', dataIndex: 'sync_task_id' },
          { title: '状态', dataIndex: 'status', render: (value) => <Tag color={value === 'SUCCESS' ? 'green' : value === 'FAILED' ? 'red' : 'blue'}>{value}</Tag> },
          { title: '进度', dataIndex: 'progress' },
          { title: '阶段', dataIndex: 'current_stage' },
        ]} />
      </SectionCard>

      <SectionCard title="本地 K线数据">
        <Table rowKey="ts" size="small" dataSource={klines} pagination={{ pageSize: 10 }} columns={[
          { title: '时间', dataIndex: 'ts' },
          { title: 'Open', dataIndex: 'open' },
          { title: 'High', dataIndex: 'high' },
          { title: 'Low', dataIndex: 'low' },
          { title: 'Close', dataIndex: 'close' },
          { title: 'Volume', dataIndex: 'volume' },
        ]} />
      </SectionCard>
    </PageContainer>
  );
}
