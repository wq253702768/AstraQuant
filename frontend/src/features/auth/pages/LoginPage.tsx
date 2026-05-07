import { LockOutlined, MailOutlined } from '@ant-design/icons';
import { Button, Checkbox, Form, Input, Select, Typography, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { routePaths } from '@/app/router/routePaths';
import { ApiError } from '@/services/request';
import styles from './LoginPage.module.css';

const { Text, Title } = Typography;

export function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const isLoading = useAuthStore((state) => state.isLoading);

  const handleLogin = async (values: { username: string; password: string }) => {
    try {
      await login(values);
      navigate(routePaths.dashboard, { replace: true });
    } catch (error) {
      const errorMessage =
        error instanceof ApiError && error.code === 'AUTH_USER_LOCKED'
          ? '登录失败次数过多，请稍后再试'
          : error instanceof Error
            ? error.message
            : '登录失败，请检查账号和密码';
      message.error(errorMessage);
    }
  };

  return (
    <main className={styles.page}>
      <section className={styles.brand}>
        <div className={styles.logo}>✦ AstraQuant 星枢量化</div>
        <Title className={styles.title}>AI 驱动的加密货币永续合约智能交易系统</Title>
        <Text className={styles.subtitle}>策略研发 · 回测验证 · AI复盘 · 风控准入 · 模拟盘验证</Text>
        <div className={styles.visual}>
          <div className={styles.curve} />
          <div className={styles.grid} />
          <div className={styles.badge}>AI 不直接下单 · 全链路审计</div>
        </div>
      </section>

      <section className={styles.panel}>
        <Title level={3}>登录工作台</Title>
        <Text type="secondary">进入 AstraQuant 策略研发与验证平台</Text>
        <Form layout="vertical" className={styles.form} onFinish={handleLogin}>
          <Form.Item label="工作区" name="workspace" initialValue="default">
            <Select
              options={[
                {
                  label: '默认工作区',
                  value: 'default',
                },
              ]}
            />
          </Form.Item>
          <Form.Item label="邮箱 / 用户名" name="username" initialValue="admin" rules={[{ required: true, message: '请输入账号' }]}>
            <Input prefix={<MailOutlined />} placeholder="admin" autoComplete="username" />
          </Form.Item>
          <Form.Item label="密码" name="password" rules={[{ required: true, message: '请输入密码' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="请输入密码" autoComplete="current-password" />
          </Form.Item>
          <div className={styles.options}>
            <Checkbox>记住登录</Checkbox>
            <a>忘记密码</a>
          </div>
          <Button type="primary" htmlType="submit" size="large" loading={isLoading} block>
            登录
          </Button>
          <Button size="large" block>
            SSO 登录
          </Button>
        </Form>
        <Text type="secondary" className={styles.notice}>
          登录后可接入 MFA 二次验证；所有关键操作均记录审计日志。
        </Text>
      </section>
    </main>
  );
}
