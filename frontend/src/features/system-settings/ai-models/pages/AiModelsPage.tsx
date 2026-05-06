import { Button, Descriptions, Table, Tag } from 'antd';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import styles from './AiModelsPage.module.css';

const models = [
  {
    name: 'DeepSeek-R1-32B',
    provider: 'DeepSeek',
    version: '20240520',
    usage: ['策略复盘', '参数优化', '反方审查'],
    context: '128K',
    temperature: 0.2,
    status: '启用',
  },
  {
    name: 'GPT-4.1',
    provider: 'OpenAI',
    version: 'latest',
    usage: ['报告生成', '策略解释'],
    context: '128K',
    temperature: 0.2,
    status: '启用',
  },
];

export function AiModelsPage() {
  return (
    <PageContainer
      title="AI模型配置"
      description="配置策略复盘、参数优化、反方审查与报告生成所使用的 AI 模型。"
      extra={<Button type="primary">新增模型</Button>}
    >
      <div className={styles.layout}>
        <SectionCard title="模型列表">
          <Table
            rowKey="name"
            dataSource={models}
            pagination={false}
            columns={[
              { title: '模型名称', dataIndex: 'name' },
              { title: '提供方', dataIndex: 'provider' },
              { title: '版本', dataIndex: 'version' },
              {
                title: '用途',
                dataIndex: 'usage',
                render: (items: string[]) => items.map((item) => <Tag key={item}>{item}</Tag>),
              },
              { title: '上下文', dataIndex: 'context' },
              { title: 'Temperature', dataIndex: 'temperature' },
              { title: '状态', dataIndex: 'status', render: (value) => <Tag color="green">{value}</Tag> },
            ]}
          />
        </SectionCard>
        <SectionCard title="模型安全约束">
          <Descriptions column={1} size="small">
            <Descriptions.Item label="AI功能">策略复盘与优化建议生成</Descriptions.Item>
            <Descriptions.Item label="是否可下单">否</Descriptions.Item>
            <Descriptions.Item label="是否可修改策略">否</Descriptions.Item>
            <Descriptions.Item label="是否进入交易热路径">否</Descriptions.Item>
            <Descriptions.Item label="输出格式">结构化 JSON + Markdown 报告</Descriptions.Item>
            <Descriptions.Item label="审计要求">每次调用生成审计ID并记录输入数据摘要</Descriptions.Item>
          </Descriptions>
          <Button className={styles.testButton}>连接测试</Button>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
