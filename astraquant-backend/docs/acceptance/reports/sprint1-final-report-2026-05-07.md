# Sprint 1 最终验收报告：基础平台 / Auth / Gateway

验收时间：2026-05-07T03:22:33Z

## 1. 验收范围

Sprint 1 当前按三部分完成：

```text
Part 1：基础登录链路真实可用
Part 2：账号安全能力
Part 3：登录失败保护与 Sprint 1 收口
```

真实验收环境：

```text
http://47.239.90.234
```

当前测试账号：

```text
username: admin
password: password
```

## 2. 当前已部署服务

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up (healthy)
```

## 3. Part 1 验收结论

报告：

```text
docs/acceptance/reports/sprint1-part1-report-2026-05-06.md
```

结果：

```text
状态：通过
P0 远程冒烟用例：9/9
```

已验证：

- 前端真实地址可访问。
- Gateway `/health` 可访问。
- 管理员账号可登录。
- 登录返回 access token 和 refresh token。
- `/api/auth/me` 返回当前用户。
- refresh token 可刷新 access token。
- 未携带 token 访问受保护 API 被拒绝。
- 前端主布局已通过浏览器级坐标验证。

## 4. Part 2 验收结论

报告：

```text
docs/acceptance/reports/sprint1-part2-report-2026-05-06.md
```

结果：

```text
状态：通过
P0 远程安全用例：12/12
```

已验证：

- Refresh Token hash 落库。
- Refresh Token Rotation。
- 旧 refresh token 不可复用。
- Logout 后 access token 被 Gateway 拒绝。
- Logout 后 refresh token 被拒绝。
- 修改密码成功。
- 修改密码后旧密码无法登录。
- 修改密码后旧 refresh token 失效。
- 前端支持自动 refresh、后端 logout、修改密码页面。

## 5. Part 3 验收结论

报告：

```text
docs/acceptance/reports/sprint1-part3-report-2026-05-07.md
```

结果：

```text
状态：通过
P0 登录保护用例：7/7
```

已验证：

- 错误密码累计失败次数。
- 达到 5 次失败后账号被临时锁定。
- 锁定期间正确密码也不能登录。
- 清理锁定后正确密码可登录。
- Part 1 / Part 2 回归均通过。

## 6. 当前实现与原始 V1.1 文档差异

| 原始设计 | 当前实现 | 处理 |
|---|---|---|
| 单用户管理员模式 | RBAC + admin 通配权限 | 保留，属于后续 Sprint 合理演进 |
| APISIX Gateway | FastAPI API Gateway | 保留，当前已支撑全系统 `/api/*` |
| Argon2id | bcrypt | 记录为安全专项风险 |
| `/system/health` | `/health` + `/api` 统一入口 | 保留，统一响应和 trace_id 已覆盖 |
| Refresh Token 建议实现 | 已实现 hash 落库、轮换、撤销 | 已完成增强 |
| Logout 建议实现 | 已实现 | 已完成 |
| 修改密码建议实现 | 已实现 | 已完成 |
| 登录失败保护 | 已实现 Redis 计数与锁定 | 已完成 |

## 7. 测试指标汇总

| 测试项 | 结果 |
|---|---:|
| Auth Service pytest | 7 passed |
| API Gateway pytest | 8 passed |
| Part 1 远程验收 | 9/9 passed |
| Part 2 远程验收 | 12/12 passed |
| Part 3 远程验收 | 7/7 passed |
| 前端 Docker build | passed |
| Headless Chrome 布局检查 | passed |

## 8. 剩余风险

- 当前密码哈希为 bcrypt，不是原始文档中的 Argon2id。
- staging 默认密码 `password` 为弱口令，仅用于测试环境。
- 设备/会话管理 UI 尚未实现。
- MFA 尚未实现。
- HttpOnly Cookie 尚未实现。
- APISIX 未引入，当前采用 FastAPI API Gateway。

## 9. 最终验收结论

状态：通过。

Sprint 1 “基础平台 / Auth / Gateway”已满足当前验收口径：

```text
用户能真实登录；
Token 安全闭环可用；
前端主框架可用；
Gateway 鉴权可用；
账号安全基础能力可用；
登录失败保护可用；
真实服务器地址验收通过。
```

可以进入 Sprint 2：Strategy Service 验收完善。
