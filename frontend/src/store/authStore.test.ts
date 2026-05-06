// @vitest-environment jsdom
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { useAuthStore } from './authStore';
import { authApi } from '@/services/auth.api';

vi.mock('@/services/auth.api', () => ({
  authApi: {
    login: vi.fn(),
    me: vi.fn(),
    refresh: vi.fn(),
  },
}));

const mockedAuthApi = vi.mocked(authApi);

describe('authStore', () => {
  beforeEach(() => {
    localStorage.clear();
    useAuthStore.getState().logout();
    vi.clearAllMocks();
  });

  it('logs in with real API response and persists tokens', async () => {
    mockedAuthApi.login.mockResolvedValue({
      access_token: 'access-token',
      refresh_token: 'refresh-token',
      expires_in: 7200,
      user: {
        id: 'user-1',
        username: 'admin',
        display_name: '管理员',
        roles: ['admin'],
      },
    });
    mockedAuthApi.me.mockResolvedValue({
      id: 'user-1',
      username: 'admin',
      display_name: '管理员',
      roles: ['admin'],
      permissions: ['*'],
    });

    await useAuthStore.getState().login({ username: 'admin', password: 'password' });

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.user?.username).toBe('admin');
    expect(state.permissions).toEqual(['*']);
    expect(localStorage.getItem('astraquant_access_token')).toBe('access-token');
    expect(localStorage.getItem('astraquant_refresh_token')).toBe('refresh-token');
  });

  it('clears auth state on logout', () => {
    localStorage.setItem('astraquant_access_token', 'access-token');
    localStorage.setItem('astraquant_refresh_token', 'refresh-token');

    useAuthStore.getState().logout();

    expect(useAuthStore.getState().isAuthenticated).toBe(false);
    expect(localStorage.getItem('astraquant_access_token')).toBeNull();
    expect(localStorage.getItem('astraquant_refresh_token')).toBeNull();
  });
});
