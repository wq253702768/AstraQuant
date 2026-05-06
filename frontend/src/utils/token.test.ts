import { beforeEach, describe, expect, it } from 'vitest';

import type { CurrentUser } from '@/types/auth';
import {
  clearAuthStorage,
  getStoredAccessToken,
  getStoredRefreshToken,
  getStoredUser,
  setAuthTokens,
  setStoredUser,
} from './token';

const user: CurrentUser = {
  id: 'u001',
  username: 'admin',
  display_name: '管理员',
  roles: ['admin'],
  permissions: ['*'],
};

describe('token storage helpers', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('stores and clears auth tokens', () => {
    setAuthTokens('access-token', 'refresh-token');

    expect(getStoredAccessToken()).toBe('access-token');
    expect(getStoredRefreshToken()).toBe('refresh-token');

    clearAuthStorage();

    expect(getStoredAccessToken()).toBeNull();
    expect(getStoredRefreshToken()).toBeNull();
  });

  it('stores current user payload', () => {
    setStoredUser(user);

    expect(getStoredUser()).toEqual(user);
  });
});
