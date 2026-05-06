import { Layout } from 'antd';
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

  if (!isAuthenticated) {
    return <Navigate to={routePaths.login} replace state={{ from: location }} />;
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
