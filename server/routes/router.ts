import type { IncomingMessage, ServerResponse } from 'node:http';

import { HttpError, sendError } from '../utils/http.js';

export interface RequestContext {
  req: IncomingMessage;
  url: URL;
  params: string[];
}

export type RouteHandler = (context: RequestContext, response: ServerResponse) => unknown | Promise<unknown>;

export interface RouteDefinition {
  method: string;
  pattern: RegExp;
  handler: RouteHandler;
}

export function createRouter(routes: RouteDefinition[]) {
  return {
    async handle(req: IncomingMessage, res: ServerResponse, url: URL): Promise<void> {
      const pathname = url.pathname.replace(/\/$/, '') || '/';
      const route = routes.find((item) => item.method === req.method && item.pattern.test(pathname));

      if (!route) {
        sendError(res, new HttpError(404, 'NOT_FOUND', '接口不存在'));
        return;
      }

      const match = pathname.match(route.pattern);

      try {
        await route.handler(
          {
            req,
            url,
            params: match ? match.slice(1).map(decodeURIComponent) : [],
          },
          res,
        );
      } catch (error) {
        sendError(res, error);
      }
    },
  };
}
