import { Navigate, createBrowserRouter } from 'react-router-dom';
import { BasicLayout } from '@/layouts/BasicLayout/BasicLayout';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { StrategyListPage } from '@/features/strategy-center/strategies/pages/StrategyListPage';
import { StrategyTemplateListPage } from '@/features/strategy-center/templates/pages/StrategyTemplateListPage';
import { StrategyTemplateDetailPage } from '@/features/strategy-center/templates/pages/StrategyTemplateDetailPage';
import { StrategyDetailPage } from '@/features/strategy-center/strategies/pages/StrategyDetailPage';
import { StrategyConfigPage } from '@/features/strategy-center/config/pages/StrategyConfigPage';
import { StrategyVersionsPage } from '@/features/strategy-center/versions/pages/StrategyVersionsPage';
import { NewBacktestPage } from '@/features/strategy-center/backtests/pages/NewBacktestPage';
import { DataValidationPage } from '@/features/strategy-center/validation/pages/DataValidationPage';
import { BacktestExecutionPage } from '@/features/strategy-center/execution/pages/BacktestExecutionPage';
import { BacktestResultPage } from '@/features/strategy-center/results/pages/BacktestResultPage';
import { BacktestTradesPage } from '@/features/strategy-center/trades/pages/BacktestTradesPage';
import { CostAnalysisPage } from '@/features/strategy-center/costs/pages/CostAnalysisPage';
import { StrategyDrawdownPage } from '@/features/strategy-center/drawdowns/pages/StrategyDrawdownPage';
import { DrawdownReplayPage } from '@/features/strategy-center/replay/pages/DrawdownReplayPage';
import { AiReviewPage } from '@/features/strategy-center/ai-review/pages/AiReviewPage';
import { OptimizationPage } from '@/features/strategy-center/optimization/pages/OptimizationPage';
import { StrategyScorePage } from '@/features/strategy-center/scoring/pages/StrategyScorePage';
import { BacktestReportPage } from '@/features/strategy-center/reports/pages/BacktestReportPage';
import { PaperValidationPage } from '@/features/strategy-center/paper-validation/pages/PaperValidationPage';
import { SystemSettingsPage } from '@/features/system-settings/overview/pages/SystemSettingsPage';
import { ExchangeSettingsPage } from '@/features/system-settings/exchange/pages/ExchangeSettingsPage';
import { AiModelsPage } from '@/features/system-settings/ai-models/pages/AiModelsPage';
import { AuditLogsPage } from '@/features/system-settings/audit-logs/pages/AuditLogsPage';
import { RiskSettingsPage } from '@/features/system-settings/risk/pages/RiskSettingsPage';
import { UsersPage } from '@/features/system-settings/users/pages/UsersPage';
import { RolesPage } from '@/features/system-settings/roles/pages/RolesPage';
import { NotificationsPage } from '@/features/system-settings/notifications/pages/NotificationsPage';
import { ChangePasswordPage } from '@/features/system-settings/password/pages/ChangePasswordPage';

export const router = createBrowserRouter([
  {
    path: '/auth/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <BasicLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'strategy-center', element: <Navigate to="/strategy-center/strategies" replace /> },
      { path: 'strategy-center/strategies', element: <StrategyListPage /> },
      { path: 'strategy-center/templates', element: <StrategyTemplateListPage /> },
      { path: 'strategy-center/templates/:templateId', element: <StrategyTemplateDetailPage /> },
      { path: 'strategy-center/strategies/:strategyId', element: <StrategyDetailPage /> },
      { path: 'strategy-center/strategies/:strategyId/config', element: <StrategyConfigPage /> },
      { path: 'strategy-center/strategies/:strategyId/versions', element: <StrategyVersionsPage /> },
      { path: 'strategy-center/strategies/:strategyId/versions/:versionId/config', element: <StrategyConfigPage /> },
      { path: 'strategy-center/backtests/new', element: <NewBacktestPage /> },
      { path: 'strategy-center/backtests/:taskId/validation', element: <DataValidationPage /> },
      { path: 'strategy-center/backtests/:taskId/execution', element: <BacktestExecutionPage /> },
      { path: 'strategy-center/backtests/:taskId/result', element: <BacktestResultPage /> },
      { path: 'strategy-center/backtests/:taskId/trades', element: <BacktestTradesPage /> },
      { path: 'strategy-center/backtests/:taskId/costs', element: <CostAnalysisPage /> },
      { path: 'strategy-center/backtests/:taskId/drawdowns', element: <StrategyDrawdownPage /> },
      { path: 'strategy-center/backtests/:taskId/replay', element: <DrawdownReplayPage /> },
      { path: 'strategy-center/backtests/:taskId/ai-review', element: <AiReviewPage /> },
      { path: 'strategy-center/backtests/:taskId/optimization', element: <OptimizationPage /> },
      { path: 'strategy-center/backtests/:taskId/score', element: <StrategyScorePage /> },
      { path: 'strategy-center/backtests/:taskId/report', element: <BacktestReportPage /> },
      { path: 'strategy-center/paper-validation', element: <PaperValidationPage /> },
      { path: 'system-settings', element: <SystemSettingsPage /> },
      { path: 'system-settings/exchange', element: <ExchangeSettingsPage /> },
      { path: 'system-settings/ai-models', element: <AiModelsPage /> },
      { path: 'system-settings/risk', element: <RiskSettingsPage /> },
      { path: 'system-settings/audit-logs', element: <AuditLogsPage /> },
      { path: 'system-settings/users', element: <UsersPage /> },
      { path: 'system-settings/roles', element: <RolesPage /> },
      { path: 'system-settings/notifications', element: <NotificationsPage /> },
      { path: 'system-settings/password', element: <ChangePasswordPage /> },
    ],
  },
]);
