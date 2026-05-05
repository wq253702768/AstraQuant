import type {
  BacktestMetric,
  CostMetric,
  Strategy,
  StrategyVersion,
  TradeRecord,
} from '../types.js';

export const strategies: Strategy[] = [
  {
    id: 'str_eth_mean_v3',
    name: 'ETH 均值回归 v3',
    type: '均值回归',
    currentVersion: 'v3.2.0',
    instId: 'ETH-USDT-SWAP',
    timeframe: '1H',
    leverage: 10,
    totalReturn: 34.21,
    maxDrawdown: -12.45,
    winRate: 63.88,
    score: 78.6,
    status: 'allowed_paper',
    riskLevel: 'medium',
  },
  {
    id: 'str_btc_breakout',
    name: 'BTC 趋势突破策略',
    type: '趋势突破',
    currentVersion: 'v1.3.2',
    instId: 'BTC-USDT-SWAP',
    timeframe: '15m',
    leverage: 10,
    totalReturn: 128.56,
    maxDrawdown: -14.63,
    winRate: 62.34,
    score: 81.4,
    status: 'allowed_paper',
    riskLevel: 'medium',
  },
  {
    id: 'str_eth_grid',
    name: 'ETH 网格震荡策略',
    type: '网格',
    currentVersion: 'v2.1.0',
    instId: 'ETH-USDT-SWAP',
    timeframe: '5m',
    leverage: 5,
    totalReturn: -5.64,
    maxDrawdown: -21.37,
    winRate: 48.2,
    score: 59.8,
    status: 'optimize',
    riskLevel: 'high',
  },
];

export const versions: StrategyVersion[] = [
  {
    id: 'ver_132',
    version: 'v1.3.2',
    status: 'pending',
    codeHash: 'a1b2c3d4...9f8e7d6c',
    createdAt: '2024-05-01 12:23',
    createdBy: '量化研究员',
    paramsSummary: '突破确认 3 根K线，杠杆 10x，止损 1.2%',
    isCurrent: true,
  },
  {
    id: 'ver_131',
    version: 'v1.3.1',
    status: 'backtested',
    codeHash: '9f8e7d6c',
    createdAt: '2024-04-26 18:42',
    createdBy: '量化研究员',
    paramsSummary: '突破确认 2 根K线，杠杆 12x，止损 1.5%',
  },
  {
    id: 'ver_130',
    version: 'v1.3.0',
    status: 'archived',
    codeHash: '6a5b4c3d',
    createdAt: '2024-04-20 09:15',
    createdBy: '系统生成',
    paramsSummary: 'ATR 突破，杠杆 8x，止盈 2.8%',
  },
];

export const backtestMetrics: BacktestMetric[] = [
  { label: '总收益率', value: '+128.56%', trend: 'positive', extra: '年化收益 85.72%' },
  { label: '最大回撤', value: '14.63%', trend: 'negative', extra: '发生于 2024-03-18' },
  { label: '胜率', value: '62.34%', trend: 'positive', extra: '231 胜 / 140 负' },
  { label: '盈亏比', value: '1.78', trend: 'neutral', extra: '平均盈利 / 平均亏损' },
  { label: 'Profit Factor', value: '1.89', trend: 'positive', extra: '总盈利 / 总亏损' },
  { label: '最大连续亏损', value: '6 笔', trend: 'negative', extra: '风险可控' },
  { label: '手续费合计', value: '-2146.32', trend: 'negative', extra: 'USDT' },
  { label: '资金费影响', value: '+1382.67', trend: 'positive', extra: 'USDT' },
];

export const costMetrics: CostMetric[] = [
  { label: '手续费', value: '1,245.36', unit: 'USDT', ratio: '占收益 8.72%' },
  { label: '滑点', value: '862.14', unit: 'USDT', ratio: '占收益 6.04%' },
  { label: '资金费', value: '-315.77', unit: 'USDT', ratio: '占收益 -2.21%' },
  { label: '买卖价差', value: '536.72', unit: 'USDT', ratio: '占收益 3.76%' },
  { label: '总成本', value: '2,328.45', unit: 'USDT', ratio: '占收益 16.31%' },
];

export const trades: TradeRecord[] = [
  {
    id: 'ord_001',
    time: '2024-05-28 17:00',
    instId: 'BTC-USDT-SWAP',
    action: '开仓',
    direction: '做多',
    leverage: '10x',
    orderType: '限价',
    fillPrice: 67418.6,
    fee: -5.24,
    slippage: -2.1,
    pnl: 366.85,
    status: '通过',
  },
  {
    id: 'ord_002',
    time: '2024-05-29 21:00',
    instId: 'BTC-USDT-SWAP',
    action: '止损',
    direction: '做多',
    leverage: '10x',
    orderType: 'IOC',
    fillPrice: 69720,
    fee: -6.1,
    slippage: -4.25,
    pnl: -639.95,
    status: '通过',
  },
];

export const lineData = [10, 18, 16, 28, 34, 31, 46, 52, 48, 63, 72, 89, 84, 102, 128];
