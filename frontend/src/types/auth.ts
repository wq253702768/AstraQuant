export interface ApiResponse<T> {
  code: string;
  message: string;
  trace_id?: string | null;
  data: T;
}

export type ApiEnvelope<T> = ApiResponse<T>;

export interface LoginRequest {
  username: string;
  password: string;
}

export interface CurrentUser {
  id: string;
  username: string;
  display_name: string;
  roles: string[];
  permissions: string[];
}

export interface LoginUser {
  id: string;
  username: string;
  display_name: string;
  roles: string[];
  permissions?: string[];
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  user: LoginUser;
}

export interface RefreshTokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

export interface LogoutRequest {
  refresh_token: string;
}

export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
}

export interface OperationSuccessResponse {
  success: boolean;
}
