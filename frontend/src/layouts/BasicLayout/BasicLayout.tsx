import { Layout, Spin } from 'antd';
import { useEffect } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { TopHeader } from './TopHeader';
import { routePaths } from '@/app/router/routePaths';
import { useAuthStore } from '@/store/authStore';
import styles from './BasicLayout.module.css';

const { Content } = Layout;

export function BasicLayout() {
  const location = useLocation();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isHydrating = useAuthStore((state) => state.isHydrating);
  const loadCurrentUser = useAuthStore((state) => state.loadCurrentUser);

  useEffect(() => {
    if (isAuthenticated) {
      void loadCurrentUser().catch(() => undefined);
    }
  }, [isAuthenticated, loadCurrentUser]);

  if (!isAuthenticated) {
    return <Navigate to={routePaths.login} replace state={{ from: location }} />;
  }

  if (isHydrating) {
    return (
      <Layout className={styles.shell}>
        <Spin fullscreen tip="正在恢复登录态..." />
      </Layout>
    );
  }

  return (
    <Layout className={styles.shell}>
      <Sidebar />
      <Layout className={styles.main}>
        <TopHeader />
        <Content className={styles.content}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
