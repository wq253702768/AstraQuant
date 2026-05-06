import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function DrawdownReplayPage() {
  return (
    <AnalysisPlaceholderPage
      title="回撤回放"
      description="播放器式还原回撤期间的 K 线、交易事件、风控事件和最大回撤点。"
      activeMetric="最大回撤 -18.93%"
      actionText="导出片段报告"
    />
  );
}
