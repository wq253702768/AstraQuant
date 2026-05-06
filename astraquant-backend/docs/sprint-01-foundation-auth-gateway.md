# Sprint 1：项目基础框架 + Auth Service + API Gateway

本 Sprint 只交付后端工程地基、认证服务和 API Gateway，不开发策略、回测、交易所接入和实盘交易。

## 验收主线

1. Docker Compose 启动 PostgreSQL、Redis、NATS、MinIO。
2. Auth Service 可启动并提供 `/health`。
3. API Gateway 可启动并提供 `/health`。
4. 默认管理员可创建。
5. 管理员可通过 Gateway 登录。
6. 登录返回 access_token 和 refresh_token。
7. access_token 可访问 `/api/auth/me`。
8. 无 Token 访问受保护接口返回 `UNAUTHORIZED`。
9. 所有响应包含 `trace_id`。
10. WebSocket `/api/ws/tasks` 可连接。
