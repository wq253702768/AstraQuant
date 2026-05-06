# Strategy Lifecycle Center

Strategy Lifecycle Center 负责策略从草稿、回测、AI 复盘、评分、模拟盘、小仓实盘到扩大仓位、回退、暂停和归档的治理闭环。

本服务只管理生命周期状态、阶段门禁、证据链和审批，不直接下单、撤单、调杠杆或解除熔断。

## 本地启动

```bash
pip install -e ../../shared/python
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8023
```

Worker:

```bash
celery -A app.workers.celery_app worker -Q lifecycle -l info
```

## 主要接口

- `GET /health`
- `GET /lifecycle/strategies`
- `GET /lifecycle/strategies/{strategy_version_id}`
- `GET /lifecycle/strategies/{strategy_version_id}/timeline`
- `GET /lifecycle/strategies/{strategy_version_id}/evidence`
- `POST /lifecycle/strategies/{strategy_version_id}/gates/evaluate`
- `POST /lifecycle/strategies/{strategy_version_id}/applications/small-live`
- `POST /lifecycle/strategies/{strategy_version_id}/applications/scale-up`
- `POST /lifecycle/approvals/{approval_id}/approve`
- `POST /lifecycle/approvals/{approval_id}/reject`
- `POST /lifecycle/strategies/{strategy_version_id}/rollback-to-paper`
- `POST /lifecycle/strategies/{strategy_version_id}/pause`
- `POST /lifecycle/strategies/{strategy_version_id}/retire`
- `GET /lifecycle/dashboard/overview`
