export interface SyncTask {
  sync_task_id: string;
  status: string;
  progress: number;
  current_stage?: string | null;
  error_message?: string | null;
  inserted_count?: number | null;
  updated_count?: number | null;
}

export interface CreateSyncTaskPayload {
  exchange: string;
  symbols: string[];
  data_types: string[];
  timeframes: string[];
  start_time?: string;
  end_time?: string;
  force_resync?: boolean;
}

export interface Kline {
  ts: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
  quote_volume: string;
}
