# Sprint 1 Part 1 测试报告：基础登录链路真实可用

测试时间：2026-05-06T11:51:50Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint1-auth-gateway-p1-45f5` |
| 部署提交 | `0f3ebb9` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Auth Service | `http://47.239.90.234/api/auth/*` |
| 部署方式 | Sprint 1 Part 1 最小栈 |

本次只部署 Sprint 1 Part 1 必需服务：

```text
postgres
redis
auth-service
api-gateway
frontend-web
```

## 2. 服务状态

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up (healthy)
```

## 3. 自动化测试结果

### 3.1 本地可执行测试

| 测试项 | 结果 |
|---|---|
| Auth Service pytest | 4 passed |
| API Gateway pytest | 7 passed |
| deploy script bash syntax | passed |
| acceptance script bash syntax | passed |
| git diff check | passed |

### 3.2 前端构建

前端构建在 staging Docker 构建过程中执行：

```text
npm ci
npm run build
```

结果：通过。

### 3.3 真实服务器地址验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_FRONTEND_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint1_part1_remote_auth.sh
```

结果：

```text
[PASS] Gateway health
[PASS] Frontend page
[PASS] Login returned SUCCESS
[PASS] Login returned access and refresh tokens
[PASS] Current user returned SUCCESS
[PASS] Current user matches login user
[PASS] Refresh token returned SUCCESS
[PASS] Refresh returned new access token
[PASS] Protected API rejects missing token
```

### 3.4 浏览器级布局验收

使用 headless Chrome 打开真实地址 `http://47.239.90.234/dashboard`，注入真实登录态后读取 DOM 布局位置。

结果：

```text
aside.top = 0
aside.left = 0
aside.height = 1013
header.top = 0
header.left = 264
main.top = 56
main.left = 264
pageTitle.top = 76
pageTitle.text = 总览大盘
LAYOUT_CHECK_PASS
```

结论：主框架已经恢复为左侧栏 + 右侧内容的横向布局，内容区不再被侧边栏高度挤到首屏底部。

## 4. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 API 用例 | 7 | 7 | 100% |
| P0 远程冒烟用例 | 9 | 9 | 100% |
| P0 后端/Gateway 自动化 | 11 | 11 | 100% |
| P0 浏览器布局验收 | 1 | 1 | 100% |

## 5. 已验证能力

- 前端真实地址可访问。
- Gateway `/health` 可通过真实地址访问。
- 管理员账号可登录。
- 登录返回 `access_token`。
- 登录返回 `refresh_token`。
- `access_token` 可访问 `/api/auth/me`。
- `/api/auth/me` 返回当前登录用户。
- `refresh_token` 可刷新 `access_token`。
- 未携带 token 访问受保护 API 会被拒绝。
- 前端 Docker 构建通过。
- 登录后 Dashboard 浏览器级布局验收通过。

## 6. 本次修复记录

- 前端从 `demo-token` 改为真实 `/api/auth/login`。
- 新增 token 存储、Auth API、Axios 请求封装。
- Header 改为展示真实用户并支持本地登出。
- 新增 Sprint 1 最小 staging compose，避免全系统构建压垮服务器。
- 修复 Auth Service Alembic 缺少 PostgreSQL 同步驱动问题。
- 修复 API Gateway live monitor 配置字段兼容问题。
- 前端 Nginx 改为 80 端口统一入口，并代理 `/api/*` 与 `/health` 到 API Gateway。
- 修复前端构建参数默认指向 `:8000` 导致浏览器登录失败的问题；当前统一通过 `http://47.239.90.234` 访问前端和 API。
- 修复登录页、侧边栏、主内容区、卡片标题的 CSS Module 类名不匹配问题，恢复真实平台页面排版。

## 7. 剩余风险

- 后端 logout 接口尚未实现，当前前端登出为清理本地 token。
- 修改密码尚未实现。
- Refresh Token 尚未落库、未 hash、未撤销。
- Token 自动刷新尚未接入前端拦截器。
- 密码哈希当前为 bcrypt，不是原始文档中的 Argon2id。
- 当前管理员初始密码仍为 `password`，后续应统一默认密码策略并要求首次修改。

## 8. 验收结论

状态：通过。

Sprint 1 Part 1 “基础登录链路真实可用”已经满足本阶段 P0 验收标准，可以进入 Sprint 1 Part 2：账号安全能力。
