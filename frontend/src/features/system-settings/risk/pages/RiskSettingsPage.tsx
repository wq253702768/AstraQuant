import { SettingsPlaceholderPage } from '../../shared/SettingsPlaceholderPage';

export function RiskSettingsPage() {
  return (
    <SettingsPlaceholderPage
      title="风控参数"
      description="管理单笔亏损、日亏损、最大回撤、强平距离、资金费率过滤等系统级风控规则。"
      items={['单笔最大亏损', '日亏损限制', '最大回撤阈值', '资金费率过滤', '强平距离预警']}
    />
  );
}
