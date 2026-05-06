# Backtest Service

高速回测服务，负责创建异步回测任务、执行策略回测引擎、输出交易明细、净值曲线、回撤区间和结果摘要。

## 本地启动

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8004
```

## Worker

```bash
celery -A app.workers.celery_app worker -Q backtest -l info
```
