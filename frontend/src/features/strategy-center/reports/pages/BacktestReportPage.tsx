import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function BacktestReportPage() {
  return (
    <AnalysisPlaceholderPage
      title="回测报告"
      description="汇总回测指标、交易摘要、成本分析、回撤复盘、AI结论与策略评分，支持 HTML / JSON / PDF 导出。"
      metrics={[
        { label: '总收益率', value: '+128.56%' },
        { label: '最大回撤', value: '-14.63%', trend: 'down' },
        { label: '策略评分', value: '78.6' },
        { label: '报告状态', value: '已生成' },
      ]}
      sections={['报告摘要', '核心指标', '图表区', 'AI复盘摘要', '策略评分', '导出操作']}
    />
  );
}
