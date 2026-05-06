import axios, { AxiosError } from 'axios';
import type { ApiEnvelope } from '@/types/auth';
import { clearAuthStorage, getAccessToken } from '@/utils/token';

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
  (error: AxiosError<ApiEnvelope<unknown>>) => {
    const status = error.response?.status;
    const envelope = error.response?.data;
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
