# Market Data Service

历史行情数据服务，负责通过 Exchange Access Gateway 同步 OKX 合约规格、K线、资金费率、标记价格，并沉淀为 PostgreSQL/ClickHouse 中的可信数据源。

## 本地启动

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## Worker

```bash
celery -A app.workers.celery_app worker -Q market_data -l info
```
