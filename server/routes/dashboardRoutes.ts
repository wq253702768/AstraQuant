import type { RouteDefinition } from './router.js';
import { getDashboardOverview } from '../services/strategyService.js';
import { sendSuccess } from '../utils/http.js';

export const dashboardRoutes: RouteDefinition[] = [
  {
    method: 'GET',
    pattern: /^\/api\/dashboard\/summary$/,
    handler: (_context, response) => {
      sendSuccess(response, getDashboardOverview());
    },
  },
];
