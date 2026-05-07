import { request } from './request';
import type { CreateSyncTaskPayload, Kline, SyncTask } from '@/types/market-data';

export const marketDataApi = {
  health() {
    return request.get<unknown, { status: string; service: string }>('/api/market-data/health');
  },
  createSyncTask(payload: CreateSyncTaskPayload) {
    return request.post<unknown, { sync_task_id: string; status: string }>('/api/market-data/sync', payload);
  },
  runSyncTask(taskId: string) {
    return request.post<unknown, { sync_task_id: string; status: string; inserted_count: number; updated_count: number }>(`/api/market-data/sync/${taskId}/run`, {});
  },
  listSyncTasks() {
    return request.get<unknown, { items: SyncTask[]; total: number }>('/api/market-data/sync');
  },
  getSyncTask(taskId: string) {
    return request.get<unknown, SyncTask>(`/api/market-data/sync/${taskId}`);
  },
  candles(params: { exchange: string; symbol: string; timeframe: string; start_time?: string; end_time?: string; limit?: number }) {
    return request.get<unknown, { items: Kline[] }>('/api/market-data/klines', { params });
  },
};
