import type { LoginResponse } from '../types.js';

const DEMO_USER = {
  id: 'u-demo',
  name: '张三',
  role: '量化研究员',
  permissions: ['*'],
};

export function createDemoSession(): LoginResponse {
  return {
    token: 'demo-token',
    user: DEMO_USER,
    permissions: DEMO_USER.permissions,
  };
}
