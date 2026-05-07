# Sprint 2 Part 1 测试报告：策略主体与模板

测试时间：2026-05-07T05:10:32Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint2-strategy-core-p1-45f5` |
| 部署提交 | `5594f6f` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Strategy Service | `http://47.239.90.234/api/strategies*` |
| 部署方式 | Sprint 2 Part 1 最小栈 |

部署服务：

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-strategy-service staging-strategy-service Up
astraquant-nats nats:latest Up
astraquant-auth-service staging-auth-service Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up (healthy)
```

## 2. 本地自动化测试

| 测试项 | 结果 |
|---|---|
| Strategy Service pytest | 7 passed |
| API Gateway pytest | 9 passed |
| Sprint 2 deploy script syntax | passed |
| Sprint 2 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址 API 验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint2_part1_strategy_core.sh
```

结果：

```text
[PASS] login
[PASS] strategy list rejects missing token
[PASS] list strategy templates
[PASS] create strategy
[PASS] duplicate strategy code rejected
[PASS] query strategy list
[PASS] query strategy detail
[PASS] update strategy
[PASS] copy strategy
[PASS] archive strategy
[PASS] query archived strategy
[PASS] archived strategy status confirmed
```

## 4. 前端浏览器级验收

使用 headless Chrome 打开真实地址并进入：

```text
http://47.239.90.234/strategy-center/strategies
```

验证结果：

```text
FRONTEND_STRATEGY_LIST_CHECK_PASS
```

关键断言：

```text
h1 = 策略列表
buttons 包含 新建策略
rows = 2
真实请求：
  GET /api/strategies
  GET /api/strategy-templates
  GET /api/auth/me
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 API/Gateway 用例 | 12 | 12 | 100% |
| P0 前端浏览器用例 | 3 | 3 | 100% |
| 后端/Gateway 自动化测试 | 16 | 16 | 100% |

## 6. 已验证能力

- Strategy Service 可启动。
- Strategy Service migration 可执行。
- 策略模板 seed 可执行。
- 策略模板可通过 Gateway 查询。
- 无 token 访问策略接口会被 Gateway 拒绝。
- 管理员 token 可创建策略。
- 策略 code 唯一约束生效。
- 策略列表可查询。
- 策略详情可查询。
- 策略基础信息可更新。
- 策略可复制。
- 策略可归档。
- 归档后详情状态为 `ARCHIVED`。
- 前端策略列表页已接入真实 API。

## 7. 本次修复记录

- Strategy Service 增加 `ACTIVE` / `ARCHIVED` 状态。
- Strategy model 增加 `latest_version_id`、`updated_by`、`archived_at`。
- Strategy Template 增加 `template_type`、`default_config`、`sort_order`。
- 新增 `strategy_audit_event_basic` 表。
- 创建策略支持可选模板，并默认使用首个启用模板。
- 新增策略基础信息更新、归档、复制接口。
- Gateway 新增策略 update/archive/copy 代理。
- 前端策略列表和详情页由 mock 数据切换为真实 API。
- 新增 Sprint 2 最小 staging compose/deploy 脚本。
- 新增 Sprint 2 真实地址验收脚本。
- Strategy Service 使用独立 `alembic_version_strategy` 版本表，避免与 Auth Service migration 冲突。
- Sprint 2 最小栈加入 NATS，避免策略创建时事件发布阻塞。

## 8. 剩余风险

- 策略版本完整配置编辑、发布、发布后不可变尚未在 Part 1 完成，进入 Part 2/Part 3。
- 轻量审计表已创建，但审计查询页面未做。
- 前端创建策略弹窗当前覆盖基础字段，复杂版本配置页在 Part 2 完善。
- 当前 Strategy Service 与 Auth Service 共用同一 PostgreSQL，已通过独立 Alembic version table 隔离迁移版本。

## 9. 验收结论

状态：通过。

Sprint 2 Part 1 “策略主体与模板”已满足本阶段 P0 验收标准，可以进入 Sprint 2 Part 2：策略版本与配置校验。
