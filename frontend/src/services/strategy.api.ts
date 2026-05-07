import { request } from './request';
import type {
  CreateStrategyPayload,
  CopyStrategyPayload,
  StrategyDetail,
  StrategyListResponse,
  StrategyTemplateResponse,
  UpdateStrategyPayload,
} from '@/types/strategy';

export const strategyApi = {
  templates() {
    return request.get<unknown, StrategyTemplateResponse>('/api/strategy-templates');
  },
  list(params?: Record<string, unknown>) {
    return request.get<unknown, StrategyListResponse>('/api/strategies', { params });
  },
  create(payload: CreateStrategyPayload) {
    return request.post<unknown, { id: string; strategy_id: string; strategy_version_id: string; status: string }>('/api/strategies', payload);
  },
  detail(strategyId: string) {
    return request.get<unknown, StrategyDetail>(`/api/strategies/${strategyId}`);
  },
  update(strategyId: string, payload: UpdateStrategyPayload) {
    return request.put<unknown, StrategyDetail>(`/api/strategies/${strategyId}`, payload);
  },
  archive(strategyId: string, reason: string) {
    return request.post<unknown, { strategy_id: string; status: string }>(`/api/strategies/${strategyId}/archive`, { reason });
  },
  copy(strategyId: string, payload: CopyStrategyPayload) {
    return request.post<unknown, { id: string; strategy_id: string; strategy_version_id: string; status: string }>(`/api/strategies/${strategyId}/copy`, payload);
  },
};
