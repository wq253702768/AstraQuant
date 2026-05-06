# AI Analysis Service

智能复盘分析服务。Sprint 7 提供 AI 任务、Prompt 版本、智能体输出、模型调用日志、Mock 多智能体编排和结构化输出校验。

## 本地启动

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8006
```

## Worker

```bash
celery -A app.workers.celery_app worker -Q ai_analysis -l info
```
