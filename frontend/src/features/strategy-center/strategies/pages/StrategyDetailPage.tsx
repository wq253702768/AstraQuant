import { Button, Form, Input, Modal, Space, Table, Tag, message } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { SettingOutlined } from '@ant-design/icons';
import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { routePaths } from '@/app/router/routePaths';
import { strategyApi } from '@/services/strategy.api';
import type { StrategyDetail, UpdateStrategyPayload } from '@/types/strategy';
import styles from './StrategyDetailPage.module.css';

export function StrategyDetailPage() {
  const { strategyId } = useParams();
  const navigate = useNavigate();
  const [strategy, setStrategy] = useState<StrategyDetail | null>(null);
  const [editing, setEditing] = useState(false);
  const [createVersionOpen, setCreateVersionOpen] = useState(false);
  const [form] = Form.useForm<UpdateStrategyPayload>();
  const [versionForm] = Form.useForm<{ change_reason: string; source_version_id?: string }>();

  const load = async () => {
    if (!strategyId) return;
    const result = await strategyApi.detail(strategyId);
    setStrategy(result);
    form.setFieldsValue({
      name: result.name,
      description: result.description || '',
      tags: Array.isArray(result.tags) ? result.tags : [],
    });
  };

  useEffect(() => {
    void load();
  }, [strategyId]);

  if (!strategy) {
    return <PageContainer title="策略详情">加载中...</PageContainer>;
  }

  const handleUpdate = async (values: UpdateStrategyPayload & { tags?: string | string[] }) => {
    const tags = typeof values.tags === 'string'
      ? values.tags.split(',').map((item) => item.trim()).filter(Boolean)
      : values.tags;
    await strategyApi.update(strategy.id, { ...values, tags });
    message.success('策略信息已更新');
    setEditing(false);
    await load();
  };

  const handleArchive = async () => {
    await strategyApi.archive(strategy.id, '策略详情页归档');
    message.success('策略已归档');
    await load();
  };

  const handleCreateVersion = async (values: { change_reason: string; source_version_id?: string }) => {
    const result = await strategyApi.createVersion(strategy.id, values);
    message.success('策略版本已创建');
    setCreateVersionOpen(false);
    versionForm.resetFields();
    navigate(routePaths.strategyCenter.strategyVersionConfig.replace(':strategyId', strategy.id).replace(':versionId', result.strategy_version_id));
  };

  return (
    <PageContainer
      title={strategy.name}
      description={strategy.description || '策略基础信息、版本摘要与状态。'}
      extra={
        <Space>
          <Button icon={<SettingOutlined />} onClick={() => setEditing((value) => !value)}>
            编辑基础信息
          </Button>
          <Button type="primary" onClick={() => setCreateVersionOpen(true)}>新建版本</Button>
          <Button danger disabled={strategy.status === 'ARCHIVED'} onClick={handleArchive}>归档策略</Button>
          <Button onClick={() => navigate('/strategy-center/strategies')}>返回列表</Button>
        </Space>
      }
    >
      <section className={styles.hero}>
        <div>
          <Space wrap>
            <Tag color={strategy.status === 'ARCHIVED' ? 'default' : 'green'}>{strategy.status}</Tag>
            <Tag color="purple">{strategy.strategy_type}</Tag>
            {(Array.isArray(strategy.tags) ? strategy.tags : []).map((tag) => <Tag key={tag}>{tag}</Tag>)}
          </Space>
          <p>策略编码：{strategy.code}</p>
        </div>
        <div className={styles.admission}>最新版本：{strategy.latest_version_id || '暂无'}</div>
      </section>

      {editing && (
        <SectionCard title="编辑基础信息">
          <Form form={form} layout="vertical" onFinish={handleUpdate}>
            <Form.Item name="name" label="策略名称" rules={[{ required: true, message: '请输入策略名称' }]}>
              <Input />
            </Form.Item>
            <Form.Item name="description" label="策略说明">
              <Input.TextArea rows={3} />
            </Form.Item>
            <Form.Item name="tags" label="标签">
              <Input placeholder="多个标签可在 Part 2 中增强为标签选择器" />
            </Form.Item>
            <Button type="primary" htmlType="submit">保存</Button>
          </Form>
        </SectionCard>
      )}

      <div className={styles.metricGrid}>
        <MetricCard title="策略状态" value={strategy.status} tone={strategy.status === 'ARCHIVED' ? 'warning' : 'success'} />
        <MetricCard title="策略类型" value={strategy.strategy_type} />
        <MetricCard title="版本数量" value={strategy.versions.length} tone="primary" />
      </div>

      <SectionCard title="版本历史摘要">
          <Table
            size="small"
            pagination={false}
            rowKey="id"
            dataSource={strategy.versions}
            columns={[
              { title: '版本', dataIndex: 'version' },
              { title: '状态', dataIndex: 'status', render: (value) => <Tag>{value}</Tag> },
              { title: '参数 Hash', dataIndex: 'params_hash' },
              {
                title: '操作',
                render: (_, record) => (
                  <Button type="link" onClick={() => navigate(routePaths.strategyCenter.strategyVersionConfig.replace(':strategyId', strategy.id).replace(':versionId', record.id))}>
                    配置
                  </Button>
                ),
              },
            ]}
          />
      </SectionCard>

      <Modal title="新建策略版本" open={createVersionOpen} onCancel={() => setCreateVersionOpen(false)} onOk={() => versionForm.submit()} destroyOnClose>
        <Form form={versionForm} layout="vertical" onFinish={handleCreateVersion} initialValues={{ source_version_id: strategy.latest_version_id }}>
          <Form.Item name="source_version_id" label="来源版本">
            <Input placeholder="默认使用当前最新版本" />
          </Form.Item>
          <Form.Item name="change_reason" label="变更原因" rules={[{ required: true, message: '请输入变更原因' }]}>
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </PageContainer>
  );
}
