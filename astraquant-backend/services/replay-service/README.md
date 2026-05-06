# Replay Service

回撤回放服务，负责从回测交易、净值曲线和回撤区间构建时间轴事件，并提供回放页面、事件窗口、K线、曲线与 JSON 导出接口。

## 本地启动

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8005
```

## Worker

```bash
celery -A app.workers.celery_app worker -Q replay -l info
```
