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
  AppstoreOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
  SettingOutlined,
  SlidersOutlined,
  StockOutlined,
  ThunderboltOutlined,
  ToolOutlined,
  UserSwitchOutlined,
  LockOutlined,
  HistoryOutlined,
  LineChartOutlined,
  PlayCircleOutlined,
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
      { key: strategy.templates, icon: <AppstoreOutlined />, label: '策略模板' },
      { key: 'strategy-config-entry', icon: <SlidersOutlined />, label: '策略配置（从详情进入）', disabled: true },
      { key: 'strategy-versions-entry', icon: <HistoryOutlined />, label: '策略版本（从详情进入）', disabled: true },
      { key: strategy.newBacktest, icon: <PlayCircleOutlined />, label: '新建回测（待验收）', disabled: true },
      { key: strategy.validation.replace(':taskId', 'bt-demo'), icon: <SafetyCertificateOutlined />, label: '数据校验（待验收）', disabled: true },
      { key: strategy.execution.replace(':taskId', 'bt-demo'), icon: <ThunderboltOutlined />, label: '回测执行（待验收）', disabled: true },
      { key: strategy.result.replace(':taskId', 'bt-demo'), icon: <LineChartOutlined />, label: '回测结果（待验收）', disabled: true },
      { key: strategy.trades.replace(':taskId', 'bt-demo'), icon: <FileTextOutlined />, label: '交易明细（待验收）', disabled: true },
      { key: strategy.costs.replace(':taskId', 'bt-demo'), icon: <BarChartOutlined />, label: '成本分析（待验收）', disabled: true },
      { key: strategy.drawdowns.replace(':taskId', 'bt-demo'), icon: <ControlOutlined />, label: '策略回撤（待验收）', disabled: true },
      { key: strategy.replay.replace(':taskId', 'bt-demo'), icon: <PlayCircleOutlined />, label: '回撤回放（待验收）', disabled: true },
      { key: strategy.aiReview.replace(':taskId', 'bt-demo'), icon: <RobotOutlined />, label: 'AI策略复盘（待验收）', disabled: true },
      { key: strategy.optimization.replace(':taskId', 'bt-demo'), icon: <DeploymentUnitOutlined />, label: '参数优化（待验收）', disabled: true },
      { key: strategy.score.replace(':taskId', 'bt-demo'), icon: <AuditOutlined />, label: '策略评分（待验收）', disabled: true },
      { key: strategy.report.replace(':taskId', 'bt-demo'), icon: <FileTextOutlined />, label: '回测报告（待验收）', disabled: true },
      { key: strategy.paperValidation, icon: <DatabaseOutlined />, label: '模拟盘验证（待验收）', disabled: true },
    ],
  },
  {
    key: routePaths.marketData,
    icon: <DatabaseOutlined />,
    label: '历史行情',
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
      { key: settings.password, icon: <LockOutlined />, label: '修改密码' },
      { key: settings.users, icon: <UserSwitchOutlined />, label: '用户管理' },
      { key: settings.roles, icon: <SafetyCertificateOutlined />, label: '角色权限' },
      { key: settings.notifications, icon: <ControlOutlined />, label: '通知设置' },
    ],
  },
];
