# Sprint 1 Part 3 测试报告：登录失败保护

测试时间：2026-05-07T03:22:33Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint1-auth-gateway-p1-45f5` |
| 部署提交 | `4ea8c42` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Auth Service | `http://47.239.90.234/api/auth/*` |
| 部署方式 | Sprint 1 最小栈 |

服务状态：

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up (healthy)
```

## 2. 本地自动化测试

| 测试项 | 结果 |
|---|---|
| Auth Service pytest | 7 passed |
| API Gateway pytest | 8 passed |
| Part 3 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
ASTRA_STAGING_HOST=47.239.90.234 \
ASTRA_STAGING_USER=deploy \
ASTRA_STAGING_SSH_KEY="$HOME/.ssh/astraquant_staging_ed25519" \
scripts/acceptance/sprint1_part3_login_protection.sh
```

结果：

```text
[PASS] bad password attempt 1 rejected
[PASS] bad password attempt 2 rejected
[PASS] bad password attempt 3 rejected
[PASS] bad password attempt 4 rejected
[PASS] bad password attempt 5 locks account
[PASS] correct password rejected while locked
[PASS] login succeeds after clearing lock
```

Part 1 回归：

```text
9/9 passed
```

Part 2 回归：

```text
12/12 passed
```

## 4. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 Part 3 登录保护用例 | 7 | 7 | 100% |
| P0 Part 1 回归用例 | 9 | 9 | 100% |
| P0 Part 2 回归用例 | 12 | 12 | 100% |
| Auth/Gateway 自动化测试 | 15 | 15 | 100% |

## 5. 已验证能力

- 错误密码会累计失败次数。
- 达到 5 次失败后账号被 Redis 临时锁定。
- 锁定期间正确密码也无法登录。
- 清理锁定 key 后正确密码可登录。
- 登录保护不破坏 Part 1 登录链路。
- 登录保护不破坏 Part 2 logout / refresh / 修改密码链路。

## 6. 本次修复记录

- 新增登录失败保护配置项。
- 新增 `LoginProtectionService`。
- 登录前检查锁定状态。
- 密码错误时增加失败计数。
- 达到阈值后写入锁定 key。
- 登录成功后清理失败计数和锁定状态。
- 锁定事件写入基础审计。
- 前端登录页针对 `AUTH_USER_LOCKED` 展示明确提示。
- 新增 Part 3 真实地址验收脚本。

## 7. 剩余风险

- 当前密码哈希为 bcrypt，不是原始设计中的 Argon2id。
- staging 默认密码 `password` 为弱口令，仅用于测试环境。
- 设备/会话管理页面尚未实现。
- MFA / HttpOnly Cookie 尚未实现。

## 8. 验收结论

状态：通过。

Sprint 1 Part 3 “登录失败保护 + 验收收口”已满足本阶段 P0 验收标准。
