import { Menu } from 'antd';
import { StarOutlined } from '@ant-design/icons';
import { useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { appMenuItems } from '@/config/menu';
import { useAppStore } from '@/store/appStore';
import styles from './BasicLayout.module.css';

function getOpenKeys(pathname: string) {
  if (pathname.startsWith('/strategy-center')) {
    return ['strategy-center'];
  }
  if (pathname.startsWith('/system-settings')) {
    return ['system-settings'];
  }
  return [];
}

export function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const collapsed = useAppStore((state) => state.sidebarCollapsed);

  const selectedKeys = useMemo(() => [location.pathname], [location.pathname]);

  return (
    <aside className={collapsed ? styles.sidebarCollapsed : styles.sidebar}>
      <div className={styles.brand}>
        <div className={styles.brandMark}>
          <StarOutlined />
        </div>
        {!collapsed && (
          <div>
            <strong>AstraQuant</strong>
            <span>星枢量化</span>
          </div>
        )}
      </div>
      <Menu
        className={styles.menu}
        defaultOpenKeys={getOpenKeys(location.pathname)}
        inlineCollapsed={collapsed}
        items={appMenuItems}
        mode="inline"
        selectedKeys={selectedKeys}
        onClick={({ key }) => navigate(String(key))}
      />
      <div className={styles.sidebarFooter}>{collapsed ? 'AQ' : '策略研发 · 回测验证 · AI复盘'}</div>
    </aside>
  );
}
