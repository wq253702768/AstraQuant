# AstraQuant Staging Server Deployment Plan

目标服务器：`47.239.90.234`

本文档定义 AstraQuant 开发/验收环境的服务器部署方式。该环境用于每次阶段性交付后的平台级联调、测试工程师验收和回归验证。

## 1. 安全原则

服务器密码、私钥、数据库密码、JWT 密钥等敏感信息不得写入：

- Git 仓库
- README
- PR 描述
- Docker Compose 文件
- Shell 脚本默认值
- CI 日志

推荐使用 SSH Key 登录：

```text
本地/CI Secret 中保存私钥
  ↓
SSH 登录 staging 服务器
  ↓
服务器从 Git 仓库拉取代码或接收 rsync 发布包
  ↓
docker compose 构建并启动服务
```

如果当前服务器仍使用密码登录，应尽快完成：

1. 创建专用部署用户，例如 `deploy`。
2. 配置 SSH 公钥登录。
3. 禁止 root 密码远程登录，或至少限制来源 IP。
4. 将 SSH 私钥放入安全 Secret，不进入仓库。

## 2. 服务器目录规划

建议目录：

```text
/opt/astraquant/
├── app/                  # 服务器上的仓库同步目录
├── env/                  # 服务器本地环境变量，不入 Git
├── logs/                 # 运维日志
├── backups/              # 数据库和配置备份
└── releases/             # 后续可选发布包目录
```

当前第一阶段采用：

```text
/opt/astraquant/app
```

作为仓库目录。

## 3. 服务器基础依赖

服务器需要：

- Git
- Docker Engine
- Docker Compose plugin
- curl
- rsync
- bash

可使用：

```bash
ASTRA_STAGING_HOST=47.239.90.234 \
ASTRA_STAGING_USER=deploy \
ASTRA_STAGING_SSH_KEY=/path/to/private_key \
  ./scripts/deploy/staging_remote_bootstrap.sh
```

在远端执行基础依赖检查和 Docker 安装。

## 4. 环境变量

服务器本地保存：

```text
/opt/astraquant/env/.env.staging
```

仓库只提供模板：

```text
deploy/staging/.env.staging.example
```

首次部署时：

```bash
cp deploy/staging/.env.staging.example /opt/astraquant/env/.env.staging
```

然后在服务器上手工修改真实密钥。

## 5. 部署命令

本地或 CI 设置：

```bash
export ASTRA_STAGING_HOST=47.239.90.234
export ASTRA_STAGING_USER=deploy
export ASTRA_STAGING_SSH_KEY=/path/to/private_key
export ASTRA_STAGING_BRANCH=cursor/sprint20-strategy-lifecycle-center-45f5
```

执行：

```bash
./scripts/deploy/staging_deploy.sh
```

脚本会：

1. 确认远程目录。
2. 同步当前仓库到服务器。
3. 确认 `/opt/astraquant/env/.env.staging` 存在。
4. 执行 `docker compose build`。
5. 执行 `docker compose up -d`。
6. 执行数据库迁移和管理员初始化。
7. 执行健康检查。

## 6. 健康检查

部署后执行：

```bash
ASTRA_STAGING_HOST=47.239.90.234 ./scripts/deploy/staging_healthcheck.sh
```

默认检查：

- API Gateway `/health`
- Auth Service `/health`
- Strategy Service `/health`
- Backtest Service `/health`
- Strategy Lifecycle Center `/health`
- Frontend Web `/`

后续每个 Sprint 完善时，应把该 Sprint 的关键健康检查和验收 API 加入脚本。

## 7. 每次交付部署流程

每次 Sprint 完善或修复交付后，固定流程：

```text
1. 自动化测试通过
2. 提交并推送代码
3. 更新 PR
4. 部署到 staging 服务器
5. 执行健康检查
6. 测试工程师执行 Sprint 验收用例
7. 记录验收结果
```

## 8. 当前限制

当前 Cursor Cloud 环境没有 `docker` 命令，因此本地无法执行镜像构建验证。构建验证应在：

- staging 服务器
- 或具备 Docker 的 CI 环境

中执行。

## 9. 不在本阶段做的事情

- 不直接把服务器密码写入任何自动化脚本。
- 不把 staging 当生产环境。
- 不自动修改交易所实盘密钥。
- 不自动启用真实交易。
- 不自动解除任何 Kill Switch。

