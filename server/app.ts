import { createServer as createHttpServer } from 'node:http';
import type { IncomingMessage, ServerResponse } from 'node:http';

import { authRoutes } from './routes/authRoutes.js';
import { dashboardRoutes } from './routes/dashboardRoutes.js';
import { createRouter } from './routes/router.js';
import { strategyRoutes } from './routes/strategyRoutes.js';
import { sendJson } from './utils/http.js';

export const router = createRouter([...authRoutes, ...dashboardRoutes, ...strategyRoutes]);

export async function handleRequest(req: IncomingMessage, res: ServerResponse): Promise<void> {
  const origin = process.env.CORS_ORIGIN ?? '*';

  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const requestUrl = new URL(req.url ?? '/', `http://${req.headers.host ?? 'localhost'}`);

  if (requestUrl.pathname === '/health') {
    sendJson(res, 200, {
      success: true,
      message: 'ok',
      data: {
        status: 'ok',
        service: 'astraquant-api',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
      },
    });
    return;
  }

  await router.handle(req, res, requestUrl);
}

export function createServer() {
  return createHttpServer((req, res) => {
    handleRequest(req, res).catch((error) => {
      sendJson(res, 500, {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: error instanceof Error ? error.message : '服务器内部错误。',
        },
      });
    });
  });
}
