import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function StrategyDrawdownPage() {
  return (
    <AnalysisPlaceholderPage
      title="策略回撤"
      description="联动策略净值曲线、回撤曲线、回撤区间与 AI 归因，定位策略风险来源。"
      metrics={[
        { label: '最大回撤', value: '-5.6%', color: 'red' },
        { label: '平均回撤', value: '-2.1%', color: 'red' },
        { label: '当前回撤', value: '-1.8%', color: 'red' },
        { label: '最大连续亏损', value: '4 次', color: 'orange' },
      ]}
      sections={[
        '左侧回测配置上下文',
        '净值曲线与交易事件标记',
        '回撤曲线与最大回撤点',
        '回撤区间列表、AI复盘、报告 Tab',
      ]}
    />
  );
}
