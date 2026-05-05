import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function OptimizationPage() {
  return (
    <AnalysisPlaceholderPage
      title="参数优化"
      description="承接 AI 优化建议，人工确认后生成新策略版本并重新回测。"
      activeTab="参数优化"
      metrics={[
        { title: '旧版本评分', value: '72.6', suffix: '/100' },
        { title: '新版本预期评分', value: '81.4', suffix: '/100', trend: '+8.8' },
        { title: '最大回撤改善', value: '+4.67', suffix: '%' },
        { title: '建议采纳项', value: '4', suffix: '项' },
      ]}
      conclusion="AI 建议降低杠杆、提高突破确认阈值并增加低流动性时段过滤。所有建议必须保存为新版本并重新回测后才可进入准入评估。"
    />
  );
}
