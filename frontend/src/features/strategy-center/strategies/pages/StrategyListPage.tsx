import { Button, Form, Input, Modal, Select, Space, Table, Tag, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { routePaths } from '@/app/router/routePaths';
import { strategyApi } from '@/services/strategy.api';
import type { CreateStrategyPayload, StrategyListItem, StrategyTemplate } from '@/types/strategy';
import styles from './StrategyListPage.module.css';

function tagsOf(tags: StrategyListItem['tags']): string[] {
  if (!tags) return [];
  return Array.isArray(tags) ? tags : Object.values(tags).map(String);
}

export function StrategyListPage() {
  const navigate = useNavigate();
  const [items, setItems] = useState<StrategyListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [templates, setTemplates] = useState<StrategyTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [keyword, setKeyword] = useState('');
  const [status, setStatus] = useState<string | undefined>();
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm<CreateStrategyPayload>();

  const load = async () => {
    setLoading(true);
    try {
      const [strategyResult, templateResult] = await Promise.all([
        strategyApi.list({ keyword: keyword || undefined, status }),
        strategyApi.templates(),
      ]);
      setItems(strategyResult.items);
      setTotal(strategyResult.total);
      setTemplates(templateResult.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const handleArchive = async (record: StrategyListItem) => {
    Modal.confirm({
      title: '确认归档该策略？',
      content: '归档后该策略不再建议用于后续回测、模拟盘或实盘流程。已发布版本和历史记录仍会保留。',
      okText: '确认归档',
      okButtonProps: { danger: true },
      cancelText: '取消',
      onOk: async () => {
        await strategyApi.archive(record.id, '策略中心页面归档');
        message.success('策略已归档');
        await load();
      },
    });
  };

  const handleCopy = async (record: StrategyListItem) => {
    Modal.confirm({
      title: '确认复制该策略？',
      content: '系统将复制策略基础信息，并基于最新版本生成一个新的草稿版本。',
      okText: '确认复制',
      cancelText: '取消',
      onOk: async () => {
        const suffix = Date.now().toString().slice(-5);
        await strategyApi.copy(record.id, {
          name: `${record.name} - 副本`,
          code: `${record.code}_copy_${suffix}`,
        });
        message.success('策略已复制');
        await load();
      },
    });
  };

  const columns: ColumnsType<StrategyListItem> = useMemo(
    () => [
      {
        title: '策略名称',
        dataIndex: 'name',
        render: (name, record) => (
          <Space direction="vertical" size={2}>
            <strong>{name}</strong>
            <span className={styles.muted}>{record.code}</span>
          </Space>
        ),
      },
      { title: '策略类型', dataIndex: 'strategy_type' },
      { title: '最新版本', dataIndex: 'latest_version', render: (value) => value || '-' },
      { title: '状态', dataIndex: 'status', render: (value) => <Tag color={value === 'ARCHIVED' ? 'default' : 'green'}>{value}</Tag> },
      {
        title: '标签',
        dataIndex: 'tags',
        render: (value) => (
          <Space wrap>
            {tagsOf(value).map((tag) => (
              <Tag key={tag}>{tag}</Tag>
            ))}
          </Space>
        ),
      },
      {
        title: '操作',
        key: 'action',
        render: (_, record) => (
          <Space>
            <Button type="link" onClick={() => navigate(routePaths.strategyCenter.strategyDetail.replace(':strategyId', record.id))}>
              查看
            </Button>
            <Button type="link" disabled={record.status === 'ARCHIVED'} onClick={() => handleCopy(record)}>
              复制
            </Button>
            <Button danger type="link" disabled={record.status === 'ARCHIVED'} onClick={() => handleArchive(record)}>
              归档
            </Button>
          </Space>
        ),
      },
    ],
    [navigate],
  );

  const handleCreate = async (values: CreateStrategyPayload) => {
    Modal.confirm({
      title: '确认创建策略？',
      content: '系统将基于所选模板创建策略，并生成初始草稿版本。',
      okText: '确认创建',
      cancelText: '取消',
      onOk: async () => {
        await strategyApi.create({ ...values, tags: values.tags ?? [], strategy_type: values.strategy_type || 'CONFIG' });
        message.success('策略创建成功');
        setOpen(false);
        form.resetFields();
        await load();
      },
    });
  };

  return (
    <div className="page-stack">
      <div className="page-toolbar">
        <div>
          <h1>策略列表</h1>
          <p>统一管理策略状态、回测表现、风险水平与模拟盘准入。</p>
        </div>
        <Space>
          <Button onClick={() => void load()}>刷新</Button>
          <Button type="primary" onClick={() => setOpen(true)}>新建策略</Button>
        </Space>
      </div>

      <div className="metric-grid six">
        <MetricCard title="策略总数" value={total} description="当前策略池" />
        <MetricCard title="模板数量" value={templates.length} description="内置策略模板" />
        <MetricCard title="活跃策略" value={items.filter((item) => item.status !== 'ARCHIVED').length} tone="success" />
        <MetricCard title="已归档" value={items.filter((item) => item.status === 'ARCHIVED').length} />
      </div>

      <SectionCard
        title="策略池"
        extra={
          <Space wrap>
            <Input.Search placeholder="搜索策略名 / 编码" style={{ width: 240 }} value={keyword} onChange={(event) => setKeyword(event.target.value)} onSearch={() => void load()} />
            <Select allowClear placeholder="状态" style={{ width: 140 }} value={status} onChange={setStatus} options={[{ value: 'ACTIVE', label: 'ACTIVE' }, { value: 'ARCHIVED', label: 'ARCHIVED' }]} />
            <Button onClick={() => void load()}>查询</Button>
          </Space>
        }
      >
        <Table
          rowKey="id"
          loading={loading}
          columns={columns}
          dataSource={items}
          pagination={{ total, pageSize: 20 }}
        />
      </SectionCard>

      <Modal title="新建策略" open={open} onCancel={() => setOpen(false)} onOk={() => form.submit()} destroyOnClose>
        <Form form={form} layout="vertical" onFinish={handleCreate} initialValues={{ strategy_type: 'CONFIG', tags: [] }}>
          <Form.Item name="template_id" label="策略模板">
            <Select allowClear placeholder="选择模板" options={templates.map((item) => ({ value: item.id, label: item.name }))} />
          </Form.Item>
          <Form.Item name="name" label="策略名称" rules={[{ required: true, message: '请输入策略名称' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="code" label="策略编码" rules={[{ required: true, message: '请输入策略编码' }]}>
            <Input placeholder="btc_trend_breakout" />
          </Form.Item>
          <Form.Item name="description" label="策略说明">
            <Input.TextArea rows={3} />
          </Form.Item>
          <Form.Item name="tags" label="标签">
            <Select mode="tags" placeholder="输入标签后回车" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
