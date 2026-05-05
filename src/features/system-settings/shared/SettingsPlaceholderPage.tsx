import { Card, Col, Row, Table, Tag } from 'antd';

import { PageContainer } from '@/layouts/PageContainer/PageContainer';

interface SettingsPlaceholderPageProps {
  title: string;
  description: string;
  primary?: string;
  items?: string[];
  checkpoints?: string[];
}

export function SettingsPlaceholderPage({
  title,
  description,
  primary,
  items,
  checkpoints,
}: SettingsPlaceholderPageProps) {
  const rows = (items ?? checkpoints ?? ['默认配置', '风控预设', '权限预留']).map((name, index) => ({
    key: String(index),
    name,
    status: index === 0 ? '已启用' : '已预留',
    updatedAt: '2024-06-05 15:32',
  }));

  return (
    <PageContainer title={title} description={description}>
      <Row gutter={[16, 16]}>
        <Col span={16}>
          <Card title={primary ?? title}>
            <Table
              pagination={false}
              dataSource={rows}
              columns={[
                { title: '名称', dataIndex: 'name' },
                { title: '状态', dataIndex: 'status', render: (value) => <Tag color="blue">{value}</Tag> },
                { title: '更新时间', dataIndex: 'updatedAt' },
              ]}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="建设原则">
            <p>系统设置承载交易所、AI模型、风控、审计和权限能力。</p>
            <p>第一阶段优先保证 AI 可审计、交易所配置可追溯、关键操作可记录。</p>
          </Card>
        </Col>
      </Row>
    </PageContainer>
  );
}
