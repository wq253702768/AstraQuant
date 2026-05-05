import { SettingsPlaceholderPage } from '../../shared/SettingsPlaceholderPage';

export function RolesPage() {
  return (
    <SettingsPlaceholderPage
      title="角色权限"
      description="预留 RBAC 权限配置能力，后续管理菜单权限、操作权限与数据权限。"
      checkpoints={['角色列表', '菜单权限', '操作权限', '数据权限', '权限审计']}
    />
  );
}
