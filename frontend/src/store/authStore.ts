import { create } from 'zustand';

import { authApi } from '@/services/auth.api';
import type { CurrentUser, LoginRequest } from '@/types/auth';
import {
  clearAuthStorage,
  getStoredAccessToken,
  getStoredRefreshToken,
  getStoredUser,
  setAuthTokens,
  setStoredUser,
} from '@/utils/token';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: CurrentUser | null;
  permissions: string[];
  isAuthenticated: boolean;
  isHydrating: boolean;
  isLoading: boolean;
  login: (payload: LoginRequest) => Promise<void>;
  loadCurrentUser: () => Promise<void>;
  logout: () => void;
}

function permissionsOf(user: CurrentUser | null): string[] {
  return user?.permissions ?? [];
}

const storedAccessToken = getStoredAccessToken();
const storedRefreshToken = getStoredRefreshToken();
const storedUser = getStoredUser();

export const useAuthStore = create<AuthState>((set, get) => ({
  accessToken: storedAccessToken,
  refreshToken: storedRefreshToken,
  user: storedUser,
  permissions: permissionsOf(storedUser),
  isAuthenticated: Boolean(storedAccessToken),
  isHydrating: false,
  isLoading: false,

  login: async (payload) => {
    set({ isLoading: true });
    try {
      const result = await authApi.login(payload);
      setAuthTokens(result.access_token, result.refresh_token);

      const user = await authApi.me();
      setStoredUser(user);
      set({
        accessToken: result.access_token,
        refreshToken: result.refresh_token,
        user,
        permissions: permissionsOf(user),
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      clearAuthStorage();
      set({
        accessToken: null,
        refreshToken: null,
        user: null,
        permissions: [],
        isAuthenticated: false,
        isLoading: false,
      });
      throw error;
    }
  },

  loadCurrentUser: async () => {
    if (!get().accessToken) {
      return;
    }
    set({ isHydrating: true });
    try {
      const user = await authApi.me();
      setStoredUser(user);
      set({
        user,
        permissions: permissionsOf(user),
        isAuthenticated: true,
        isHydrating: false,
      });
    } catch (error) {
      clearAuthStorage();
      set({
        accessToken: null,
        refreshToken: null,
        user: null,
        permissions: [],
        isAuthenticated: false,
        isHydrating: false,
        isLoading: false,
      });
      throw error;
    }
  },

  logout: () => {
    clearAuthStorage();
    set({
      accessToken: null,
      refreshToken: null,
      user: null,
      permissions: [],
      isAuthenticated: false,
      isHydrating: false,
      isLoading: false,
    });
  },
}));
