# AstraQuant

AstraQuant 仓库现在按前后端职责拆分：

```text
.
├── frontend/             # React + Vite + Ant Design 前端工作台
└── astraquant-backend/   # 后端 Monorepo，包含 Auth、Gateway、Strategy 等服务
```

## 前端

```bash
cd frontend
npm install
npm run dev
```

## 后端

```bash
cd astraquant-backend
docker compose up -d postgres redis nats minio
```

后端各服务的启动方式见 `astraquant-backend/README.md`。
