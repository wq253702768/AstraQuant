# AstraQuant Backend

永续合约智能交易系统正式后端 Monorepo。

Sprint 1 聚焦项目基础框架、Auth Service 与 API Gateway：

- 本地基础设施：PostgreSQL、Redis、NATS、MinIO
- Python/FastAPI 服务模板与共享公共库
- Go 服务模板
- Auth Service：用户、角色、权限、JWT、登录日志
- API Gateway：统一入口、鉴权、代理、trace_id、WebSocket 预留

## 本地启动

```bash
cd astraquant-backend
docker compose up -d postgres redis nats minio
pip install -e shared/python
pip install -e services/auth-service
pip install -e services/api-gateway
pip install -e services/strategy-service
pip install -e services/market-data-service
./scripts/migrate_all.sh
PYTHONPATH=shared/python:services/auth-service python scripts/create_admin_user.py
```

启动 Auth Service：

```bash
cd services/auth-service
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

启动 API Gateway：

```bash
cd services/api-gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动 Strategy Service：

```bash
cd services/strategy-service
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

启动 Market Data Service：

```bash
cd services/market-data-service
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

启动 Backtest Service：

```bash
cd services/backtest-service
uvicorn app.main:app --host 0.0.0.0 --port 8004
```

启动 Replay Service：

```bash
cd services/replay-service
uvicorn app.main:app --host 0.0.0.0 --port 8005
```

## Sprint 1 接口

- `GET /health`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/dashboard/overview`
- `WS /api/ws/tasks`
- `WS /api/ws/realtime`

## Sprint 3 Exchange Gateway

Exchange Access Gateway 位于 `services/exchange-access-gateway/`，默认监听 `8010`：

```bash
cd services/exchange-access-gateway
go run ./cmd/server
```

常用接口：

- `GET /health`
- `GET /metrics`
- `GET /api/v1/exchanges/OKX/time`
- `GET /api/v1/exchanges/OKX/instruments?contract_type=swap`
- `GET /api/v1/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=5m&limit=100`
- `GET /api/v1/exchanges/OKX/funding-rate?symbol=BTC-USDT-SWAP`
- `GET /api/v1/exchanges/OKX/funding-rate-history?symbol=BTC-USDT-SWAP&limit=100`
- `GET /api/v1/exchanges/OKX/mark-price?symbol=BTC-USDT-SWAP`

## Sprint 4 Market Data Service

Market Data Service 位于 `services/market-data-service/`，默认监听 `8003`。

常用接口：

- `POST /api/market-data/sync`
- `GET /api/market-data/sync/{id}`
- `GET /api/market-data/instruments`
- `GET /api/market-data/klines`
- `GET /api/market-data/funding-rates`
- `GET /api/market-data/mark-prices`
- `GET /api/market-data/quality`

Sprint 5 新增回测接口：

- `POST /api/backtests`
- `GET /api/backtests/{id}/status`
- `GET /api/backtests/{id}/summary`
- `GET /api/backtests/{id}/trades`
- `GET /api/backtests/{id}/drawdowns`
- `POST /api/backtests/{id}/cancel`

Sprint 6 新增回放服务接口：

- `POST /api/replays/build`
- `GET /api/replays/build/{id}`
- `GET /api/replays/{drawdown_id}/page`
- `GET /api/replays/{drawdown_id}/events`
- `GET /api/replays/{drawdown_id}/klines`
- `GET /api/replays/{drawdown_id}/curves`
- `GET /api/replays/{drawdown_id}/export`

Sprint 7 新增 AI 分析服务接口：

- `POST /api/ai/backtest-analysis`
- `GET /api/ai/tasks/{id}/status`
- `GET /api/ai/tasks/{id}/result`
- `GET /api/ai/tasks/{id}/model-calls`
- `GET /api/ai/prompts`

Sprint 8 新增评分与报告接口：

- `POST /api/strategy-scores/calculate`
- `GET /api/strategy-scores/{id}`
- `GET /api/strategy-versions/{id}/score/latest`
- `POST /api/reports/build`
- `GET /api/reports/tasks/{id}`
- `GET /api/reports/tasks/{id}/files`

Sprint 9 新增实时行情网关：

- `GET /health` on `services/realtime-market-gateway` port `8011`
- `GET /api/v1/runtime/status`
- `GET /api/v1/subscriptions`
- `POST /api/v1/subscriptions`
- `DELETE /api/v1/subscriptions`

Sprint 10 新增实时状态服务：

- `GET /api/state/market/{exchange}/{symbol}`
- `GET /api/state/bbo/{exchange}/{symbol}`
- `GET /api/state/trade/{exchange}/{symbol}`
- `GET /api/state/kline/{exchange}/{symbol}`
- `GET /api/state/mark-price/{exchange}/{symbol}`
- `GET /api/state/funding/{exchange}/{symbol}`
- `GET /api/state/snapshot/{exchange}/{symbol}`
- `GET /api/state/freshness/{exchange}/{symbol}`

Sprint 11 新增信号服务：

- `GET /api/signals`
- `GET /api/signals/{id}`
- `GET /api/signal-runtime/strategies`
- `POST /api/signal-runtime/reload`
- `POST /api/signal-runtime/strategies/{id}/pause`

Sprint 12 新增实时风控服务接口：

- `GET /api/risk/decisions`
- `GET /api/risk/decisions/{id}`
- `GET /api/risk/rules`
- `POST /api/risk/check`

Sprint 13 新增模拟盘交易接口：

- `POST /api/paper-trading/accounts`
- `GET /api/paper-trading/accounts/{id}`
- `GET /api/paper-trading/accounts/{id}/positions`
- `GET /api/paper-trading/accounts/{id}/ledger`
- `GET /api/paper-trading/orders`
- `GET /api/paper-trading/trades`
- `GET /api/paper-trading/performance/strategies/{id}`

Sprint 14 新增模拟盘监控服务接口：

- `POST /api/paper-monitor/observations`
- `GET /api/paper-monitor/observations/{id}`
- `GET /api/paper-monitor/dashboard/overview`
- `GET /api/paper-monitor/equity-curve`
- `GET /api/paper-monitor/strategies/{id}/daily-summary`
- `POST /api/paper-monitor/observations/{id}/admission/calculate`
- `GET /api/paper-monitor/admission-results/{id}`
- `GET /api/paper-monitor/daily-reports`

Sprint 15 新增交易所账户服务接口：

- `POST /api/exchange-accounts`
- `GET /api/exchange-accounts`
- `POST /api/exchange-accounts/{id}/credentials`
- `POST /api/exchange-accounts/{id}/test-connectivity`
- `POST /api/exchange-accounts/{id}/enable`
- `POST /api/exchange-accounts/{id}/disable`
- `GET /api/exchange-accounts/{id}/state`
- `GET /api/exchange-accounts/{id}/positions`
- `GET /api/exchange-accounts/{id}/orders`

Sprint 16 新增订单执行服务接口：

- `GET /api/order-executor/orders`
- `GET /api/order-executor/orders/{id}`
- `GET /api/order-executor/trades`
- `POST /api/order-executor/dry-run`
- `POST /api/order-executor/orders/{id}/cancel`
- `GET /api/order-executor/orders/{id}/logs`
- `POST /api/order-executor/kill-switch/trigger`
- `POST /api/order-executor/kill-switch/{id}/release`

Sprint 17 新增实盘安全控制接口：

- `GET /api/live-risk/states`
- `GET /api/live-risk/circuit-breakers`
- `GET /api/live-risk/circuit-breakers/{id}`
- `POST /api/live-risk/emergency-controls/trigger`
- `POST /api/live-risk/emergency-controls/{id}/release`
- `GET /api/live-risk/rules`

Sprint 18 新增实盘监控驾驶舱接口：

- `GET /api/live-monitor/dashboard/overview`
- `GET /api/live-monitor/accounts/{id}/summary`
- `GET /api/live-monitor/strategies/{id}/summary`
- `GET /api/live-monitor/positions`
- `GET /api/live-monitor/orders`
- `GET /api/live-monitor/trades`
- `GET /api/live-monitor/equity-curve`
- `GET /api/live-monitor/risk-events`
- `POST /api/live-monitor/observations`
- `POST /api/live-monitor/observations/{id}/admission/calculate`
- `GET /api/live-monitor/admission-results/{id}`
- `GET /api/live-monitor/comparisons/paper-live`
- `GET /api/live-monitor/daily-reports`

Sprint 19 新增告警与审计中心接口：

- `GET /api/alerts`
- `GET /api/alerts/{id}`
- `POST /api/alerts/{id}/acknowledge`
- `POST /api/alerts/{id}/resolve`
- `POST /api/alerts/suppressions`
- `GET /api/alerts/dashboard/overview`
- `GET /api/audit/events`
- `GET /api/audit/events/{id}`
- `GET /api/audit/traces/{trace_id}`
- `POST /api/audit/exports`
- `GET /api/audit/dashboard/overview`

Sprint 20 新增策略生命周期闭环中心接口：

- `GET /api/lifecycle/strategies`
- `GET /api/lifecycle/strategies/{id}`
- `GET /api/lifecycle/strategies/{id}/timeline`
- `GET /api/lifecycle/strategies/{id}/evidence`
- `POST /api/lifecycle/strategies/{id}/gates/evaluate`
- `POST /api/lifecycle/strategies/{id}/applications/small-live`
- `POST /api/lifecycle/strategies/{id}/applications/scale-up`
- `POST /api/lifecycle/approvals/{id}/approve`
- `POST /api/lifecycle/approvals/{id}/reject`
- `POST /api/lifecycle/strategies/{id}/rollback-to-paper`
- `POST /api/lifecycle/strategies/{id}/pause`
- `POST /api/lifecycle/strategies/{id}/retire`
- `GET /api/lifecycle/dashboard/overview`

Sprint 2 新增策略服务接口：

- `GET /api/strategy-templates`
- `POST /api/strategies`
- `GET /api/strategies`
- `GET /api/strategies/{id}`
- `POST /api/strategies/{id}/versions`
- `PUT /api/strategy-versions/{id}/params`
- `POST /api/strategy-versions/{id}/submit-backtest`

默认管理员账号：

- 用户名：`admin`
- 密码：`password`

所有正式 HTTP 响应遵循：

```json
{ "code": "SUCCESS", "message": "OK", "trace_id": "trace_xxx", "data": {} }
```
