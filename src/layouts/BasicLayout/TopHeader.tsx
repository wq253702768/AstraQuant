import { BellOutlined, MenuFoldOutlined, MenuUnfoldOutlined, SearchOutlined } from '@ant-design/icons';
import { Avatar, Badge, Button, Input, Select, Space, Typography } from 'antd';
import { useAppStore } from '@/store/appStore';
import styles from './BasicLayout.module.css';

export function TopHeader() {
  const collapsed = useAppStore((state) => state.sidebarCollapsed);
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);

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
        <Input prefix={<SearchOutlined />} placeholder="搜索策略、合约、指标..." className={styles.search} />
        <Select
          value="default"
          className={styles.workspace}
          options={[{ value: 'default', label: '默认工作区' }]}
        />
        <Badge count={12} size="small">
          <Button type="text" icon={<BellOutlined />} />
        </Badge>
        <Space>
          <Avatar src="https://api.dicebear.com/7.x/personas/svg?seed=zhang" />
          <Typography.Text>张三</Typography.Text>
        </Space>
      </Space>
    </header>
  );
}
