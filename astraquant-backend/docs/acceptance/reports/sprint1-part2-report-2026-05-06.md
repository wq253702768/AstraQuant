# Sprint 1 Part 2 测试报告：账号安全能力

测试时间：2026-05-06T13:31:36Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint1-auth-gateway-p1-45f5` |
| 部署提交 | `4e6c18c` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Auth Service | `http://47.239.90.234/api/auth/*` |
| 部署方式 | Sprint 1 最小栈 |

部署服务：

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
| Auth Service pytest | 6 passed |
| API Gateway pytest | 8 passed |
| Part 2 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
ASTRA_TEST_NEW_PASSWORD='NewPassword@123' \
ASTRA_STAGING_HOST=47.239.90.234 \
ASTRA_STAGING_USER=deploy \
ASTRA_STAGING_SSH_KEY="$HOME/.ssh/astraquant_staging_ed25519" \
scripts/acceptance/sprint1_part2_remote_security.sh
```

结果：

```text
[PASS] login with current password
[PASS] refresh token rotation succeeds
[PASS] old refresh token is revoked
[PASS] logout succeeds
[PASS] access token rejected after logout
[PASS] refresh token rejected after logout
[PASS] login before password change
[PASS] change password succeeds
[PASS] old password rejected
[PASS] old refresh rejected after password change
[PASS] new password login succeeds
[PASS] restore original password via staging cleanup
```

Part 1 回归：

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

## 4. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 Part 2 远程安全用例 | 12 | 12 | 100% |
| P0 Part 1 回归用例 | 9 | 9 | 100% |
| Auth/Gateway 自动化测试 | 14 | 14 | 100% |

## 5. 已验证能力

- 登录时保存 refresh token hash。
- Refresh Token Rotation 生效。
- 旧 refresh token 复用失败。
- Logout 成功。
- Logout 后 access token 被 Gateway 拒绝。
- Logout 后 refresh token 被拒绝。
- 修改密码成功。
- 旧密码登录失败。
- 修改密码后旧 refresh token 失效。
- 新密码登录成功。
- 测试完成后 staging admin 密码恢复为 `password`。

## 6. 本次修复记录

- 新增 `refresh_token` 表和基础审计表 migration。
- Auth Service 登录时保存 refresh token hash。
- Auth Service refresh 时校验 hash、撤销旧 token 并轮换新 refresh token。
- 新增 logout 接口并撤销 refresh token。
- 新增修改密码接口并撤销所有 refresh token。
- Access Token 增加 `jti`，logout/改密后加入 Redis 黑名单。
- API Gateway 鉴权时检查 Redis 黑名单。
- 前端 Axios 增加 401 自动 refresh 与原请求重试。
- 前端退出登录调用后端 logout。
- 新增系统设置中的修改密码页面。
- 新增 Part 2 远程安全验收脚本。

## 7. 剩余风险

- 登录失败次数锁定仍未实现，建议放入 Sprint 1 Part 3 或 Part 2 后续增强。
- 当前密码哈希为 bcrypt，不是原始设计中的 Argon2id。
- 当前 staging 默认密码 `password` 为弱口令，仅用于测试环境。
- Refresh Token 已落库 hash，但完整设备会话管理页面尚未实现。

## 8. 验收结论

状态：通过。

Sprint 1 Part 2 “账号安全能力”已满足本阶段 P0 验收标准，可以继续推进 Sprint 1 剩余验收完善。
