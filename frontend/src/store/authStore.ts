import { create } from 'zustand';

export interface UserInfo {
  id: string;
  name: string;
  role: string;
  avatar?: string;
}

interface AuthState {
  token: string | null;
  user: UserInfo | null;
  permissions: string[];
  isAuthenticated: boolean;
  loginAsDemo: () => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('astraquant_token'),
  user: localStorage.getItem('astraquant_token')
    ? {
        id: 'u-demo',
        name: '张三',
        role: '量化研究员',
      }
    : null,
  permissions: ['*'],
  isAuthenticated: Boolean(localStorage.getItem('astraquant_token')),
  loginAsDemo: () => {
    localStorage.setItem('astraquant_token', 'demo-token');
    set({
      token: 'demo-token',
      user: {
        id: 'u-demo',
        name: '张三',
        role: '量化研究员',
      },
      permissions: ['*'],
      isAuthenticated: true,
    });
  },
  logout: () => {
    localStorage.removeItem('astraquant_token');
    set({
      token: null,
      user: null,
      permissions: [],
      isAuthenticated: false,
    });
  },
}));
