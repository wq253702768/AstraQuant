import { request } from './request';
import type { CurrentUser, LoginRequest, LoginResponse, RefreshTokenResponse } from '@/types/auth';

function login(payload: LoginRequest) {
  return request.post<unknown, LoginResponse>('/api/auth/login', payload);
}

function me() {
  return request.get<unknown, CurrentUser>('/api/auth/me');
}

function refresh(refreshToken: string) {
  return request.post<unknown, RefreshTokenResponse>('/api/auth/refresh', {
    refresh_token: refreshToken,
  });
}

export const authApi = {
  login,
  me,
  refresh,
};
