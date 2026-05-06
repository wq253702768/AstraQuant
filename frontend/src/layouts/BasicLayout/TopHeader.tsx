import { BellOutlined, LogoutOutlined, MenuFoldOutlined, MenuUnfoldOutlined, SearchOutlined } from '@ant-design/icons';
import { Avatar, Badge, Button, Input, Select, Space, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import { routePaths } from '@/app/router/routePaths';
import { useAppStore } from '@/store/appStore';
import { useAuthStore } from '@/store/authStore';
import styles from './BasicLayout.module.css';

export function TopHeader() {
  const navigate = useNavigate();
  const collapsed = useAppStore((state) => state.sidebarCollapsed);
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate(routePaths.login, { replace: true });
  };

  return (
    <header className={styles.header}>
      <Space size={14}>
        <Button
          type="text"
          icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={toggleSidebar}
        />
        <Typography.Text className={styles.breadcrumb}>AstraQuant 星枢量化</Typography.Text>
      </Space>
      <Space size={16}>
        <Input prefix={<SearchOutlined />} placeholder="搜索策略、品种、指标..." className={styles.search} />
        <Select
          value="default"
          className={styles.workspace}
          options={[{ value: 'default', label: '默认工作区' }]}
        />
        <Badge count={12} size="small">
          <Button type="text" icon={<BellOutlined />} />
        </Badge>
        <Space>
          <Avatar src={`https://api.dicebear.com/7.x/personas/svg?seed=${user?.username ?? 'admin'}`} />
          <Typography.Text>{user?.display_name || user?.username || '未登录'}</Typography.Text>
          <Button type="text" icon={<LogoutOutlined />} onClick={handleLogout}>
            退出
          </Button>
        </Space>
      </Space>
    </header>
  );
}
