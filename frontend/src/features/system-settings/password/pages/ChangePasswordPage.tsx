import { Button, Form, Input, Typography, message } from 'antd';
import { useNavigate } from 'react-router-dom';

import { routePaths } from '@/app/router/routePaths';
import { authApi } from '@/services/auth.api';
import { useAuthStore } from '@/store/authStore';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';

import styles from './ChangePasswordPage.module.css';

interface ChangePasswordForm {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

function validatePassword(password: string): boolean {
  return /[a-z]/.test(password) && /[A-Z]/.test(password) && /\d/.test(password) && /[^A-Za-z0-9]/.test(password);
}

export function ChangePasswordPage() {
  const navigate = useNavigate();
  const clearSession = useAuthStore((state) => state.clearSession);

  const handleSubmit = async (values: ChangePasswordForm) => {
    await authApi.changePassword({
      old_password: values.old_password,
      new_password: values.new_password,
    });
    message.success('密码修改成功，请使用新密码重新登录');
    clearSession();
    navigate(routePaths.login, { replace: true });
  };

  return (
    <PageContainer title="修改密码" description="修改当前登录账号密码。提交成功后将撤销当前登录态并要求重新登录。">
      <SectionCard title="账号安全">
        <Form className={styles.form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item label="当前密码" name="old_password" rules={[{ required: true, message: '请输入当前密码' }]}>
            <Input.Password autoComplete="current-password" placeholder="请输入当前密码" />
          </Form.Item>
          <Form.Item
            label="新密码"
            name="new_password"
            rules={[
              { required: true, message: '请输入新密码' },
              { min: 8, message: '新密码至少 8 位' },
              {
                validator: (_, value: string | undefined) =>
                  !value || validatePassword(value)
                    ? Promise.resolve()
                    : Promise.reject(new Error('新密码需包含大小写字母、数字和特殊字符')),
              },
            ]}
          >
            <Input.Password autoComplete="new-password" placeholder="至少 8 位，包含大小写字母、数字和特殊字符" />
          </Form.Item>
          <Form.Item
            label="确认新密码"
            name="confirm_password"
            dependencies={['new_password']}
            rules={[
              { required: true, message: '请再次输入新密码' },
              ({ getFieldValue }) => ({
                validator(_, value: string | undefined) {
                  if (!value || getFieldValue('new_password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的新密码不一致'));
                },
              }),
            ]}
          >
            <Input.Password autoComplete="new-password" placeholder="请再次输入新密码" />
          </Form.Item>
          <Typography.Paragraph type="secondary" className={styles.hint}>
            修改密码后，当前 Access Token 和所有 Refresh Token 都会失效。
          </Typography.Paragraph>
          <Button type="primary" htmlType="submit">
            修改密码
          </Button>
        </Form>
      </SectionCard>
    </PageContainer>
  );
}
