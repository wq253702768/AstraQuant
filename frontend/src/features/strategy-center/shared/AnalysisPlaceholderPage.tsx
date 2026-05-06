import { Alert, Button, Col, Row, Table, Tag } from 'antd';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import styles from './AnalysisPlaceholderPage.module.css';

interface AnalysisPlaceholderPageProps {
  title: string;
  description?: string;
  subtitle?: string;
  activeModule?: string;
  activeTab?: string;
  active?: string;
  activeKey?: string;
  activeMetric?: string;
  actionText?: string;
  metricTitles?: string[];
  metrics?: Array<Record<string, string>>;
  sections?: string[];
  conclusion?: string;
}

const columns = [
  { title: '对象', dataIndex: 'name' },
  { title: '状态', dataIndex: 'status', render: (value: string) => <Tag color="green">{value}</Tag> },
  { title: '结果', dataIndex: 'result' },
  { title: '审计ID', dataIndex: 'auditId' },
];

const dataSource = [
  { key: 1, name: 'BTC 趋势突破策略 v1.3.2', status: '已生成', result: '+34.21%', auditId: 'aq_20240520_001' },
  { key: 2, name: 'ETH 均值回归 v3.2.0', status: '待确认', result: '-12.45%', auditId: 'aq_20240520_002' },
];

export function AnalysisPlaceholderPage({
  title,
  description,
  subtitle,
  activeModule,
  activeTab,
  active,
  activeKey,
  activeMetric,
  actionText,
  metricTitles,
  metrics,
  sections,
  conclusion,
}: AnalysisPlaceholderPageProps) {
  const moduleName = activeModule ?? activeTab ?? active ?? activeKey ?? activeMetric ?? title;
  const metricLabels = metricTitles ?? metrics?.map((item) => item.title ?? item.label ?? item.value) ?? [
    '任务状态',
    '关联策略版本',
    '风险提示',
    '审计状态',
  ];

  return (
    <PageContainer
      title={title}
      description={description ?? subtitle}
      extra={[
        <Button key="report">导出报告</Button>,
        <Button key="primary" type="primary">
          {actionText ?? '新建任务'}
        </Button>,
      ]}
    >
      <Alert
        className={styles.alert}
        type="info"
        showIcon
        message={`${moduleName} 已纳入第一阶段策略中心闭环`}
        description="当前页面先按标准中后台骨架落位，后续将接入专属图表、事件链、AI审计与策略版本数据。"
      />
      <Row gutter={[16, 16]}>
        {metricLabels.slice(0, 4).map((label, index) => (
          <Col key={`${label}-${index}`} xs={24} sm={12} lg={6}>
            <MetricCard
              title={label}
              value={index === 0 ? '运行正常' : index === 1 ? 'v1.3.2' : index === 2 ? '中等' : '已记录'}
              tone={index === 2 ? 'warning' : 'success'}
            />
          </Col>
        ))}
      </Row>
      <SectionCard title={`${moduleName} 数据预览`}>
        <Table columns={columns} dataSource={dataSource} pagination={false} />
      </SectionCard>
      {sections?.length ? (
        <SectionCard title="页面模块">
          {sections.map((section) => (
            <Tag key={section} color="blue">
              {section}
            </Tag>
          ))}
        </SectionCard>
      ) : null}
      {conclusion ? <Alert type="success" showIcon message="系统结论" description={conclusion} /> : null}
    </PageContainer>
  );
}
