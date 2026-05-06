import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios';
import type { ApiEnvelope, RefreshTokenResponse } from '@/types/auth';
import { clearAuthStorage, getAccessToken, getRefreshToken, setAuthTokens } from '@/utils/token';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';

export class ApiError extends Error {
  code: string;
  status?: number;
  data?: unknown;

  constructor(message: string, code: string, status?: number, data?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
    this.data = data;
  }
}

export const request = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

let refreshPromise: Promise<string> | null = null;

interface RetriableRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

request.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

request.interceptors.response.use(
  (response) => {
    const envelope = response.data as ApiEnvelope<unknown>;
    if (envelope && typeof envelope === 'object' && 'code' in envelope) {
      if (envelope.code !== 'SUCCESS') {
        throw new ApiError(envelope.message || '请求失败', envelope.code, response.status, envelope.data);
      }
      return envelope.data;
    }
    return response.data;
  },
  async (error: AxiosError<ApiEnvelope<unknown>>) => {
    const status = error.response?.status;
    const envelope = error.response?.data;
    const originalRequest = error.config as RetriableRequestConfig | undefined;
    const isRefreshRequest = originalRequest?.url?.includes('/api/auth/refresh');
    const refreshToken = getRefreshToken();
    if (status === 401 && originalRequest && !originalRequest._retry && !isRefreshRequest && refreshToken) {
      originalRequest._retry = true;
      try {
        if (!refreshPromise) {
          refreshPromise = axios
            .post<ApiEnvelope<RefreshTokenResponse>>(
              `${API_BASE_URL}/api/auth/refresh`,
              { refresh_token: refreshToken },
              { timeout: 15000 },
            )
            .then((response) => {
              if (response.data.code !== 'SUCCESS') {
                throw new ApiError(response.data.message, response.data.code, response.status, response.data.data);
              }
              setAuthTokens(response.data.data.access_token, response.data.data.refresh_token);
              return response.data.data.access_token;
            })
            .finally(() => {
              refreshPromise = null;
            });
        }
        const newAccessToken = await refreshPromise;
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return request.request(originalRequest);
      } catch {
        clearAuthStorage();
        window.location.assign('/auth/login');
      }
    }
    if (status === 401) {
      clearAuthStorage();
    }
    throw new ApiError(
      envelope?.message || error.message || '网络请求失败',
      envelope?.code || 'NETWORK_ERROR',
      status,
      envelope?.data,
    );
  },
);
