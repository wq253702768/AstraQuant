import type { MenuProps } from 'antd';
import {
  AuditOutlined,
  BarChartOutlined,
  ControlOutlined,
  DashboardOutlined,
  DatabaseOutlined,
  DeploymentUnitOutlined,
  FileTextOutlined,
  FundProjectionScreenOutlined,
  HistoryOutlined,
  LineChartOutlined,
  PlayCircleOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
  SettingOutlined,
  SlidersOutlined,
  StockOutlined,
  ThunderboltOutlined,
  ToolOutlined,
  UserSwitchOutlined,
} from '@ant-design/icons';
import { routePaths } from '@/app/router/routePaths';

const strategy = routePaths.strategyCenter;
const settings = routePaths.systemSettings;

export type AppMenuItem = Required<MenuProps>['items'][number] & {
  permission?: string;
  children?: AppMenuItem[];
};

export const appMenuItems: AppMenuItem[] = [
  {
    key: routePaths.dashboard,
    icon: <DashboardOutlined />,
    label: '总览大盘',
  },
  {
    key: 'strategy-center',
    icon: <StockOutlined />,
    label: '策略中心',
    children: [
      { key: strategy.strategies, icon: <FundProjectionScreenOutlined />, label: '策略列表' },
      { key: strategy.strategyConfig.replace(':strategyId', 'btc-trend'), icon: <SlidersOutlined />, label: '策略配置' },
      { key: strategy.strategyVersions.replace(':strategyId', 'btc-trend'), icon: <HistoryOutlined />, label: '策略版本' },
      { key: strategy.newBacktest, icon: <PlayCircleOutlined />, label: '新建回测' },
      { key: strategy.validation.replace(':taskId', 'bt-demo'), icon: <SafetyCertificateOutlined />, label: '数据校验' },
      { key: strategy.execution.replace(':taskId', 'bt-demo'), icon: <ThunderboltOutlined />, label: '回测执行' },
      { key: strategy.result.replace(':taskId', 'bt-demo'), icon: <LineChartOutlined />, label: '回测结果' },
      { key: strategy.trades.replace(':taskId', 'bt-demo'), icon: <FileTextOutlined />, label: '交易明细' },
      { key: strategy.costs.replace(':taskId', 'bt-demo'), icon: <BarChartOutlined />, label: '成本分析' },
      { key: strategy.drawdowns.replace(':taskId', 'bt-demo'), icon: <ControlOutlined />, label: '策略回撤' },
      { key: strategy.replay.replace(':taskId', 'bt-demo'), icon: <PlayCircleOutlined />, label: '回撤回放' },
      { key: strategy.aiReview.replace(':taskId', 'bt-demo'), icon: <RobotOutlined />, label: 'AI策略复盘' },
      { key: strategy.optimization.replace(':taskId', 'bt-demo'), icon: <DeploymentUnitOutlined />, label: '参数优化' },
      { key: strategy.score.replace(':taskId', 'bt-demo'), icon: <AuditOutlined />, label: '策略评分' },
      { key: strategy.report.replace(':taskId', 'bt-demo'), icon: <FileTextOutlined />, label: '回测报告' },
      { key: strategy.paperValidation, icon: <DatabaseOutlined />, label: '模拟盘验证' },
    ],
  },
  {
    key: 'system-settings',
    icon: <SettingOutlined />,
    label: '系统设置',
    children: [
      { key: settings.overview, icon: <SettingOutlined />, label: '设置首页' },
      { key: settings.exchange, icon: <ToolOutlined />, label: '交易所配置' },
      { key: settings.aiModels, icon: <RobotOutlined />, label: 'AI模型配置' },
      { key: settings.risk, icon: <SafetyCertificateOutlined />, label: '风控参数' },
      { key: settings.auditLogs, icon: <AuditOutlined />, label: '审计日志' },
      { key: settings.users, icon: <UserSwitchOutlined />, label: '用户管理' },
      { key: settings.roles, icon: <SafetyCertificateOutlined />, label: '角色权限' },
      { key: settings.notifications, icon: <ControlOutlined />, label: '通知设置' },
    ],
  },
];
