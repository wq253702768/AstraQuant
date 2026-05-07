import { request } from './request';
import type {
  CreateStrategyPayload,
  CreateStrategyVersionPayload,
  CopyStrategyPayload,
  PublishStrategyVersionResponse,
  StrategyDetail,
  StrategyListResponse,
  StrategyTemplateResponse,
  StrategyVersionDetail,
  StrategyVersionListResponse,
  UpdateStrategyVersionParamsPayload,
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
  versions(strategyId: string) {
    return request.get<unknown, StrategyVersionListResponse>(`/api/strategies/${strategyId}/versions`);
  },
  versionDetail(strategyId: string, versionId: string) {
    return request.get<unknown, StrategyVersionDetail>(`/api/strategies/${strategyId}/versions/${versionId}`);
  },
  createVersion(strategyId: string, payload: CreateStrategyVersionPayload) {
    return request.post<unknown, { strategy_version_id: string; version: string; status: string; params_hash: string }>(`/api/strategies/${strategyId}/versions`, payload);
  },
  updateVersionParams(versionId: string, payload: UpdateStrategyVersionParamsPayload) {
    return request.put<unknown, { strategy_version_id: string; status: string; params_hash: string }>(`/api/strategy-versions/${versionId}/params`, payload);
  },
  publishVersion(strategyId: string, versionId: string, publishNote?: string) {
    return request.post<unknown, PublishStrategyVersionResponse>(`/api/strategies/${strategyId}/versions/${versionId}/publish`, { publish_note: publishNote });
  },
  copyVersion(strategyId: string, versionId: string, changeReason: string) {
    return request.post<unknown, { strategy_version_id: string; version: string; status: string; params_hash: string }>(`/api/strategies/${strategyId}/versions/${versionId}/copy`, { change_reason: changeReason });
  },
};
