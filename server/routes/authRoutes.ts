import { createDemoSession } from '../services/authService.js';
import { HttpError, parseJsonBody, sendSuccess } from '../utils/http.js';
import type { RouteDefinition } from './router.js';

export const authRoutes: RouteDefinition[] = [
  {
    method: 'POST',
    pattern: /^\/api\/auth\/demo-login$/,
    handler: async ({ req }, response) => {
      const hasBody = Number(req.headers['content-length'] ?? 0) > 0 || req.headers['transfer-encoding'] !== undefined;
      const body = hasBody ? await parseJsonBody<unknown>(req) : {};

      if (body !== undefined && (typeof body !== 'object' || body === null || Array.isArray(body))) {
        throw new HttpError(400, 'BAD_REQUEST', '请求体必须是 JSON 对象');
      }

      const session = createDemoSession();
      sendSuccess(response, session, '登录成功');
    },
  },
];
