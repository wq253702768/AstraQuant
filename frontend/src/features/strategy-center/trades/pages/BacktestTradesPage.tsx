import { AnalysisPlaceholderPage } from '../../shared/AnalysisPlaceholderPage';

export function BacktestTradesPage() {
  return (
    <AnalysisPlaceholderPage
      title="交易明细"
      subtitle="展示每笔交易的参数、订单事件链、风控结果和单笔复盘入口。"
      active="交易明细"
      metrics={[
        { title: '总交易数', value: '371 笔' },
        { title: '胜率', value: '62.34%', color: 'green' },
        { title: '手续费', value: '-2,146.32 USDT', color: 'red' },
        { title: '滑点', value: '-842.18 USDT', color: 'red' },
      ]}
    />
  );
}
