import { request } from './request';
import type {
  ChangePasswordRequest,
  CurrentUser,
  LoginRequest,
  LoginResponse,
  LogoutRequest,
  OperationSuccess,
  RefreshTokenResponse,
} from '@/types/auth';

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

function logout(payload: LogoutRequest) {
  return request.post<unknown, OperationSuccess>('/api/auth/logout', payload);
}

function changePassword(payload: ChangePasswordRequest) {
  return request.put<unknown, OperationSuccess>('/api/auth/password', payload);
}

export const authApi = {
  login,
  me,
  refresh,
  logout,
  changePassword,
};
