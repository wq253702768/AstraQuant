# AstraQuant

AstraQuant 星枢量化工作台，当前仓库包含前端工作台与一个轻量 TypeScript API 服务。

## 开发脚本

```bash
npm run dev            # 启动 Vite 前端
npm run build          # 构建前端并编译后端
npm run build:server   # 仅编译后端
npm run start:server   # 启动编译后的后端服务
npm run test           # 运行 Vitest 测试
```

后端默认监听 `0.0.0.0:8787`，可通过环境变量调整：

```bash
HOST=127.0.0.1 PORT=8787 CORS_ORIGIN=http://localhost:5173 npm run start:server
```

## 后端 API

服务端位于 `server/`，基于 Node 内置 HTTP 模块实现，返回统一 JSON 结构：

```json
{
  "success": true,
  "message": "ok",
  "data": {}
}
```

首批接口：

- `GET /health`：服务健康检查
- `POST /api/auth/demo-login`：获取演示登录会话
- `GET /api/dashboard/summary`：总览大盘指标、策略行和近期任务
- `GET /api/strategies?status=&riskLevel=&keyword=`：策略列表，支持状态、风险等级和关键词过滤
- `GET /api/strategies/:strategyId`：策略详情
- `GET /api/strategies/:strategyId/versions`：策略版本列表
- `GET /api/backtests/:taskId/metrics`：回测指标和净值曲线
- `GET /api/backtests/:taskId/costs`：回测成本分析
- `GET /api/backtests/:taskId/trades?instId=`：交易明细，支持按交易标的过滤

当前数据源为 `server/data/strategyData.ts` 中的内存示例数据，结构与前端策略中心 mock 数据保持一致，后续可替换为数据库或外部量化引擎。
