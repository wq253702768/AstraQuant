import { describe, expect, it } from 'vitest';

import { handleRequest } from './app.js';

const request = async (path: string, init?: RequestInit) => {
  const url = new URL(path, 'http://localhost');
  const webRequest = new Request(url, init);
  const response = await new Promise<Response>((resolve) => {
    const req = {
      method: webRequest.method,
      url: `${url.pathname}${url.search}`,
      headers: Object.fromEntries(webRequest.headers.entries()),
      [Symbol.asyncIterator]: async function* () {
        if (init?.body) {
          yield Buffer.from(String(init.body));
        }
      },
    };
    const chunks: Buffer[] = [];
    const res = {
      setHeader: () => undefined,
      writeHead: (_status: number, headers: HeadersInit) => {
        responseStatus = _status;
        responseHeaders = headers;
      },
      end: (chunk?: string) => {
        if (chunk) {
          chunks.push(Buffer.from(chunk));
        }
        resolve(
          new Response(Buffer.concat(chunks), {
            status: responseStatus,
            headers: responseHeaders,
          }),
        );
      },
    };
    let responseStatus = 200;
    let responseHeaders: HeadersInit = {};

    handleRequest(req as never, res as never);
  });

  return response;
};

describe('AstraQuant API', () => {
  it('returns health information', async () => {
    const response = await request('/health');
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.data.status).toBe('ok');
  });

  it('lists strategies with filters', async () => {
    const response = await request('/api/strategies?riskLevel=high');
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.data.items).toHaveLength(1);
    expect(body.data.items[0].id).toBe('str_eth_grid');
  });

  it('creates a demo auth session', async () => {
    const response = await request('/api/auth/demo-login', {
      method: 'POST',
      body: JSON.stringify({}),
    });
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.data.token).toBe('demo-token');
    expect(body.data.user.permissions).toEqual(['*']);
  });

  it('returns 404 for unknown strategy', async () => {
    const response = await request('/api/strategies/missing');
    const body = await response.json();

    expect(response.status).toBe(404);
    expect(body.error.code).toBe('NOT_FOUND');
  });
});
