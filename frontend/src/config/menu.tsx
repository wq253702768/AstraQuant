import type { MenuProps } from 'antd';
import {
  AuditOutlined,
  ControlOutlined,
  DashboardOutlined,
  FundProjectionScreenOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
  SettingOutlined,
  StockOutlined,
  ToolOutlined,
  UserSwitchOutlined,
  LockOutlined,
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
      { key: settings.password, icon: <LockOutlined />, label: '修改密码' },
      { key: settings.users, icon: <UserSwitchOutlined />, label: '用户管理' },
      { key: settings.roles, icon: <SafetyCertificateOutlined />, label: '角色权限' },
      { key: settings.notifications, icon: <ControlOutlined />, label: '通知设置' },
    ],
  },
];
