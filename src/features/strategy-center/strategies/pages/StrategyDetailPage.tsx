import { Button, Space, Table, Tag } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import { LineChartOutlined, RobotOutlined, SettingOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { SimpleLineChart } from '@/components/charts/SimpleLineChart';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { routePaths } from '@/app/router/routePaths';
import { mockStrategies, mockVersionHistory } from '../../services/mockData';
import styles from './StrategyDetailPage.module.css';

export function StrategyDetailPage() {
  const { strategyId } = useParams();
  const navigate = useNavigate();
  const strategy = mockStrategies.find((item) => item.id === strategyId) ?? mockStrategies[0];

  return (
    <PageContainer
      title={strategy.name}
      description="汇总策略版本、最近回测、风险画像、AI复盘摘要与模拟盘准入状态。"
      extra={
        <Space>
          <Button icon={<SettingOutlined />} onClick={() => navigate(`/strategy-center/strategies/${strategy.id}/config`)}>
            配置参数
          </Button>
          <Button onClick={() => navigate(`/strategy-center/strategies/${strategy.id}/versions`)}>查看版本</Button>
          <Button type="primary" icon={<ThunderboltOutlined />} onClick={() => navigate(routePaths.newBacktest)}>
            新建回测
          </Button>
        </Space>
      }
    >
      <section className={styles.hero}>
        <div>
          <Space wrap>
            <Tag color="blue">{strategy.currentVersion}</Tag>
            <Tag>{strategy.instId}</Tag>
            <Tag>{strategy.timeframe}</Tag>
            <Tag color="purple">{strategy.type}</Tag>
            <Tag color="gold">{strategy.riskLevel}</Tag>
          </Space>
          <p>
            当前版本最近回测表现稳健，最大回撤处于可接受区间。建议进入模拟盘验证，不建议直接实盘部署。
          </p>
        </div>
        <div className={styles.admission}>模拟盘准入：允许</div>
      </section>

      <div className={styles.metricGrid}>
        <MetricCard title="最近收益率" value={`${strategy.totalReturn.toFixed(2)}%`} tone="success" />
        <MetricCard title="最大回撤" value={`${strategy.maxDrawdown.toFixed(2)}%`} tone="danger" />
        <MetricCard title="胜率" value={`${strategy.winRate.toFixed(2)}%`} tone="success" />
        <MetricCard title="Profit Factor" value="1.78" tone="primary" />
        <MetricCard title="策略评分" value={`${strategy.score.toFixed(1)}/100`} tone="primary" />
        <MetricCard title="默认杠杆" value={strategy.leverage} suffix="x" />
      </div>

      <div className={styles.twoColumns}>
        <SectionCard title="最近回测净值曲线" extra="策略净值 vs 基准">
          <SimpleLineChart color="#1677ff" height={260} />
        </SectionCard>
        <SectionCard title="风险摘要" extra={<RobotOutlined />}>
          <div className={styles.riskList}>
            <div><span>最大连续亏损</span><strong>6 笔</strong></div>
            <div><span>资金费影响</span><strong className={styles.positive}>+582.37 USDT</strong></div>
            <div><span>滑点成本</span><strong className={styles.negative}>-862.14 USDT</strong></div>
            <div><span>准入建议</span><strong className={styles.positive}>进入模拟盘</strong></div>
          </div>
        </SectionCard>
      </div>

      <div className={styles.threeColumns}>
        <SectionCard title="版本历史摘要">
          <Table
            size="small"
            pagination={false}
            rowKey="id"
            dataSource={mockVersionHistory.slice(0, 3)}
            columns={[
              { title: '版本', dataIndex: 'version' },
              { title: '状态', dataIndex: 'status', render: (value) => <Tag color={value === '当前版本' ? 'blue' : 'green'}>{value}</Tag> },
            ]}
          />
        </SectionCard>
        <SectionCard title="最近回测任务">
          <div className={styles.timeline}>
            <div>BT-20240630-001 · 已完成 · +12.8%</div>
            <div>BT-20240605-153208 · 已完成 · +34.21%</div>
            <div>BT-20240517-00123 · AI复盘完成</div>
          </div>
        </SectionCard>
        <SectionCard title="AI复盘摘要" extra={<LineChartOutlined />}>
          <p className={styles.aiText}>
            策略在趋势行情中收益贡献明显，但震荡区间存在假突破亏损。建议提高突破确认阈值，降低杠杆，并继续执行模拟盘验证。
          </p>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
