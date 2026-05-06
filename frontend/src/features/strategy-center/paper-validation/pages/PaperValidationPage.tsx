import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function PaperValidationPage() {
  return (
    <AnalysisPlaceholderPage
      title="模拟盘验证"
      subtitle="在实时行情环境中验证策略稳定性、风控有效性和模拟执行结果。"
      metricTitles={['已运行天数', '模拟收益率', '风险状态', '当前持仓']}
    />
  );
}
