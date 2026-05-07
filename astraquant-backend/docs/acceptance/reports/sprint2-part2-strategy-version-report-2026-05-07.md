# Sprint 2 Part 2 测试报告：策略版本与配置校验

测试时间：2026-05-07T06:19:31Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint2-strategy-core-p1-45f5` |
| 部署提交 | `8886ad1` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Strategy Service | `http://47.239.90.234/api/strategies*` |
| 部署方式 | Sprint 2 最小栈 |

服务状态：

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-strategy-service staging-strategy-service Up
astraquant-nats nats:latest Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up (healthy)
```

## 2. 本地自动化测试

| 测试项 | 结果 |
|---|---|
| Strategy Service pytest | 7 passed |
| API Gateway pytest | 9 passed |
| Part 2 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址 API 验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint2_part2_strategy_versions.sh
```

结果：

```text
[PASS] login
[PASS] list strategy templates
[PASS] create strategy
[PASS] list initial versions
[PASS] create draft version without explicit source
[PASS] query version detail
[PASS] update draft version with valid config
[PASS] invalid symbol rejected (INVALID_STRATEGY_PARAMS)
[PASS] invalid risk config rejected (INVALID_RISK_PARAMS)
```

Part 1 回归：

```text
12/12 passed
```

## 4. 前端浏览器级验收

使用 headless Chrome 打开真实地址：

```text
http://47.239.90.234/strategy-center/strategies/{strategyId}/versions/{versionId}/config
```

验证结果：

```text
FRONTEND_VERSION_CONFIG_CHECK_PASS
```

关键断言：

```text
h1 = 策略配置 v1.0
textarea 数量 >= 2
按钮包含 保存配置
真实请求：
  GET /api/strategies/{strategyId}/versions/{versionId}
  GET /api/auth/me
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 Part 2 API 用例 | 9 | 9 | 100% |
| P0 Part 1 回归用例 | 12 | 12 | 100% |
| P0 前端浏览器用例 | 3 | 3 | 100% |
| 后端/Gateway 自动化测试 | 16 | 16 | 100% |

## 6. 已验证能力

- 可查询策略版本列表。
- 可查询策略版本详情。
- 可在不显式传 `source_version_id` 时创建新草稿版本。
- 可更新 DRAFT 版本配置。
- 合法配置保存成功。
- 非法交易品种被拒绝。
- 非法风控参数被拒绝。
- 前端策略详情页可新建版本。
- 前端版本配置页可展示并保存 JSON 配置。

## 7. 本次修复记录

- 创建策略版本支持无 `source_version_id`。
- 创建版本默认使用当前最新版本作为来源。
- 查询版本列表和版本详情 API。
- Strategy Service 避免 async SQLAlchemy lazy-load 模板导致 `MissingGreenlet`。
- 更新配置只允许 DRAFT 状态。
- 配置校验增强：
  - symbols
  - timeframe
  - trade_direction
  - indicator_config
  - entry_rule_config
  - exit_rule_config
  - risk_params_json
- Gateway 新增版本列表/详情代理。
- 前端新增版本配置页，支持 params/risk JSON 编辑。
- 前端策略详情页新增新建版本入口。

## 8. 剩余风险

- 策略版本发布和发布后不可变完整流程在 Sprint 2 Part 3 完成。
- 当前配置页使用 JSON TextArea，复杂表单化编辑后续增强。
- 当前非法 symbols 返回 `INVALID_STRATEGY_PARAMS`，后续可进一步细化为 `STRATEGY_SYMBOL_INVALID`。
- `config_hash` / published_at / published_by 仍在 Part 3 完善。

## 9. 验收结论

状态：通过。

Sprint 2 Part 2 “策略版本与配置校验”已满足本阶段 P0 验收标准，可以进入 Sprint 2 Part 3：版本发布与不可变收口。
