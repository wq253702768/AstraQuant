import type { IncomingMessage, ServerResponse } from 'node:http';

import type { ApiErrorResponse, ApiSuccessResponse } from '../types.js';

export class HttpError extends Error {
  statusCode: number;
  code: string;

  constructor(statusCode: number, code: string, message: string) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

export const json = <T>(data: T, message = 'ok'): ApiSuccessResponse<T> => ({
  success: true,
  message,
  data,
});

export const parseJsonBody = async <T>(req: IncomingMessage): Promise<T> => {
  const chunks: Buffer[] = [];

  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }

  if (chunks.length === 0) {
    return {} as T;
  }

  try {
    return JSON.parse(Buffer.concat(chunks).toString('utf8')) as T;
  } catch {
    throw new HttpError(400, 'INVALID_JSON', '请求体必须是合法 JSON。');
  }
};

export const sendJson = (res: ServerResponse, statusCode: number, payload: unknown) => {
  const body = JSON.stringify(payload);

  res.writeHead(statusCode, {
    'Access-Control-Allow-Origin': process.env.CORS_ORIGIN ?? '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
};

export const sendSuccess = <T>(res: ServerResponse, data: T, message = 'ok', statusCode = 200) => {
  sendJson(res, statusCode, json(data, message));
};

export function sendError(res: ServerResponse, error: unknown): void;
export function sendError(res: ServerResponse, statusCode: number, code: string, message: string): void;
export function sendError(
  res: ServerResponse,
  errorOrStatusCode: unknown,
  code?: string,
  explicitMessage?: string,
) {
  const statusCode =
    typeof errorOrStatusCode === 'number'
      ? errorOrStatusCode
      : errorOrStatusCode instanceof HttpError
        ? errorOrStatusCode.statusCode
        : 500;
  const errorCode =
    typeof errorOrStatusCode === 'number'
      ? (code ?? 'ERROR')
      : errorOrStatusCode instanceof HttpError
        ? errorOrStatusCode.code
        : 'INTERNAL_SERVER_ERROR';
  const message =
    typeof errorOrStatusCode === 'number'
      ? (explicitMessage ?? '请求处理失败。')
      : errorOrStatusCode instanceof Error
        ? errorOrStatusCode.message
        : '服务器内部错误。';
  const payload: ApiErrorResponse = {
    success: false,
    error: {
      code: errorCode,
      message,
    },
  };

  sendJson(res, statusCode, payload);
}
