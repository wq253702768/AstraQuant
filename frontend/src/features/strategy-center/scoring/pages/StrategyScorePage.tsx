import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function StrategyScorePage() {
  return (
    <AnalysisPlaceholderPage
      title="策略评分"
      description="基于收益能力、风险控制、交易质量、资金效率和稳定性输出模拟盘准入结论。"
      metrics={[
        { title: '综合评分', value: '78.6', suffix: '/100', trend: 'B+ 良好', tone: 'success' },
        { title: '收益能力', value: '76.3', trend: '权重 30%' },
        { title: '风险控制', value: '72.1', trend: '权重 25%', tone: 'warning' },
        { title: '进入模拟盘', value: '允许', trend: '禁止直接实盘', tone: 'success' },
      ]}
      sections={[
        '准入阶段：继续研究允许、重新回测建议、进入模拟盘允许、小仓实盘暂不建议、正式实盘禁止。',
        '评分维度与权重将使用雷达图和明细表展示。',
        '允许进入模拟盘不代表允许实盘交易。',
      ]}
    />
  );
}
