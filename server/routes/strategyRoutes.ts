import {
  getBacktestMetrics,
  getCostMetrics,
  getStrategy,
  getStrategyTrades,
  getStrategyVersions,
  listStrategies,
} from '../services/strategyService.js';
import { HttpError, sendSuccess } from '../utils/http.js';
import type { RouteDefinition } from './router.js';

export const strategyRoutes: RouteDefinition[] = [
  {
    method: 'GET',
    pattern: /^\/api\/strategies$/,
    handler: ({ url }, response) => {
      const status = url.searchParams.get('status') ?? undefined;
      const riskLevel = url.searchParams.get('riskLevel') ?? undefined;
      const keyword = url.searchParams.get('keyword') ?? undefined;
      const items = listStrategies({ status, riskLevel, keyword });

      sendSuccess(response, {
        items,
        total: items.length,
      });
    },
  },
  {
    method: 'GET',
    pattern: /^\/api\/strategies\/([^/]+)$/,
    handler: ({ params }, response) => {
      const strategy = getStrategy(params[0]);

      if (!strategy) {
        throw new HttpError(404, 'NOT_FOUND', '策略不存在');
      }

      sendSuccess(response, strategy);
    },
  },
  {
    method: 'GET',
    pattern: /^\/api\/strategies\/([^/]+)\/versions$/,
    handler: ({ params }, response) => {
      const versions = getStrategyVersions(params[0]);

      if (!versions) {
        throw new HttpError(404, 'NOT_FOUND', '策略不存在');
      }

      sendSuccess(response, { items: versions, total: versions.length });
    },
  },
  {
    method: 'GET',
    pattern: /^\/api\/backtests\/([^/]+)\/metrics$/,
    handler: ({ params }, response) => {
      sendSuccess(response, getBacktestMetrics(params[0]));
    },
  },
  {
    method: 'GET',
    pattern: /^\/api\/backtests\/([^/]+)\/costs$/,
    handler: ({ params }, response) => {
      sendSuccess(response, getCostMetrics(params[0]));
    },
  },
  {
    method: 'GET',
    pattern: /^\/api\/backtests\/([^/]+)\/trades$/,
    handler: ({ params, url }, response) => {
      const instId = url.searchParams.get('instId') ?? undefined;
      sendSuccess(response, getStrategyTrades(params[0], { instId }));
    },
  },
];
