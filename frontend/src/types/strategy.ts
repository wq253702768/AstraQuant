export interface StrategyTemplate {
  id: string;
  code: string;
  name: string;
  strategy_type: string;
  description?: string | null;
  default_config?: Record<string, unknown> | null;
}

export interface StrategyTemplateResponse {
  items: StrategyTemplate[];
  total?: number;
}

export interface StrategyListItem {
  id: string;
  name: string;
  code: string;
  strategy_type: string;
  status: string;
  tags?: string[] | Record<string, unknown> | null;
  latest_version?: string | null;
  latest_version_id?: string | null;
  created_at?: string | null;
}

export interface StrategyListResponse {
  items: StrategyListItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface StrategyVersionSummary {
  id: string;
  version: string;
  status: string;
  params_hash: string;
  created_at?: string | null;
}

export interface StrategyDetail extends StrategyListItem {
  description?: string | null;
  updated_at?: string | null;
  versions: StrategyVersionSummary[];
}

export interface CreateStrategyPayload {
  name: string;
  code: string;
  description?: string;
  strategy_type: string;
  template_id?: string;
  tags?: string[];
}

export interface UpdateStrategyPayload {
  name?: string;
  description?: string;
  tags?: string[];
}

export interface CopyStrategyPayload {
  name: string;
  code: string;
}
