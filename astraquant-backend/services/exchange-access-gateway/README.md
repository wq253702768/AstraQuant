# Exchange Access Gateway

统一交易所访问网关。Sprint 3 实现 OKX 公共 REST 数据访问、统一模型、限流、基础熔断、请求审计预留和 HTTP API。

## 本地启动

```bash
go run ./cmd/server
```

默认端口：`8010`

## API

- `GET /health`
- `GET /metrics`
- `GET /api/v1/exchanges/OKX/time`
- `GET /api/v1/exchanges/OKX/instruments?contract_type=swap&symbol=BTC-USDT-SWAP`
- `GET /api/v1/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=5m&limit=100`
- `GET /api/v1/exchanges/OKX/funding-rate?symbol=BTC-USDT-SWAP`
- `GET /api/v1/exchanges/OKX/funding-rate-history?symbol=BTC-USDT-SWAP&limit=100`
- `GET /api/v1/exchanges/OKX/mark-price?symbol=BTC-USDT-SWAP`
