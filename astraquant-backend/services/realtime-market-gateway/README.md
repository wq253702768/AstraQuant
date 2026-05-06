# Realtime Market Gateway

实时行情网关。Sprint 9 接入 OKX Public/Business WebSocket，标准化 ticker、BBO、trade、kline、mark price、funding 事件，并发布到 NATS。

## 本地启动

```bash
GOTOOLCHAIN=local go run ./cmd/server
```

默认端口：`8011`
