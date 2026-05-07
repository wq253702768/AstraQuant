import type { CurrentUser } from '@/types/auth';

const ACCESS_TOKEN_KEY = 'astraquant_access_token';
const REFRESH_TOKEN_KEY = 'astraquant_refresh_token';
const USER_KEY = 'astraquant_user';

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export const getStoredAccessToken = getAccessToken;

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export const getStoredRefreshToken = getRefreshToken;

export function setAuthTokens(accessToken: string, refreshToken?: string | null): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
}

export function clearAuthStorage(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function getStoredUser(): CurrentUser | null {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw) as CurrentUser;
  } catch {
    clearAuthStorage();
    return null;
  }
}

export function setStoredUser(user: CurrentUser): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}
