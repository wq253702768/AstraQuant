import { Button, Space, Table, Tag } from 'antd';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';
import { MetricCard } from '@/components/data-display/MetricCard';
import { routePaths } from '@/app/router/routePaths';
import { strategyApi } from '@/services/strategy.api';
import type { StrategyTemplate } from '@/types/strategy';

export function StrategyTemplateListPage() {
  const navigate = useNavigate();
  const [items, setItems] = useState<StrategyTemplate[]>([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const result = await strategyApi.templates();
      setItems(result.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  return (
    <div className="page-stack">
      <div className="page-toolbar">
        <div>
          <h1>策略模板</h1>
          <p>模板当前为只读。若需自定义策略，请基于模板创建策略后编辑策略版本配置。</p>
        </div>
        <Button onClick={() => void load()}>刷新</Button>
      </div>

      <div className="metric-grid">
        <MetricCard title="模板数量" value={items.length} description="当前启用模板" />
        <MetricCard title="模板模式" value="只读" description="暂不允许直接编辑模板" />
        <MetricCard title="自定义方式" value="版本配置" description="通过策略版本 JSON 调整" />
        <MetricCard title="删除策略" value="归档" description="不做物理删除" />
      </div>

      <SectionCard title="模板列表">
        <Table
          rowKey="id"
          loading={loading}
          dataSource={items}
          pagination={false}
          columns={[
            {
              title: '模板名称',
              dataIndex: 'name',
              render: (name, record) => (
                <Space direction="vertical" size={2}>
                  <strong>{name}</strong>
                  <span className="muted">{record.code}</span>
                </Space>
              ),
            },
            { title: '策略类型', dataIndex: 'strategy_type' },
            { title: '描述', dataIndex: 'description' },
            { title: '状态', render: () => <Tag color="green">启用</Tag> },
            {
              title: '操作',
              render: (_, record) => (
                <Button type="link" onClick={() => navigate(routePaths.strategyCenter.templateDetail.replace(':templateId', record.id))}>
                  查看详情
                </Button>
              ),
            },
          ]}
        />
      </SectionCard>
    </div>
  );
}
