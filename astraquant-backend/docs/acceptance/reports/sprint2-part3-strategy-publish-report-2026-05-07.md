# Sprint 2 Part 3 测试报告：策略版本发布与不可变收口

测试时间：2026-05-07T06:44:25Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint2-strategy-core-p1-45f5` |
| 部署提交 | `6edf993` |
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
| Strategy Service pytest | 8 passed |
| API Gateway pytest | 9 passed |
| Part 3 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址 API 验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint2_part3_strategy_publish.sh
```

结果：

```text
[PASS] login
[PASS] create strategy
[PASS] publish draft version
[PASS] published version has config hash
[PASS] query published version detail
[PASS] query strategy after publish
[PASS] strategy latest_version_id updated
[PASS] published version rejects params update (STRATEGY_VERSION_ALREADY_PUBLISHED)
[PASS] copy published version as draft
[PASS] query copied draft version
[PASS] copied version is draft
```

回归结果：

```text
Sprint 2 Part 1：12/12 passed
Sprint 2 Part 2：9/9 passed
```

## 4. 前端浏览器级验收

使用 headless Chrome 打开真实地址：

```text
http://47.239.90.234/strategy-center/strategies/{strategyId}/versions/{versionId}/config
```

验证结果：

```text
FRONTEND_PUBLISHED_VERSION_CHECK_PASS
```

关键断言：

```text
h1 = 策略配置 v1.0
页面包含 PUBLISHED
按钮包含 复制为新草稿
params_json / risk_params_json 文本框均为 readOnly
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 Part 3 API 用例 | 11 | 11 | 100% |
| P0 Part 1 回归用例 | 12 | 12 | 100% |
| P0 Part 2 回归用例 | 9 | 9 | 100% |
| P0 前端浏览器用例 | 4 | 4 | 100% |
| 后端/Gateway 自动化测试 | 17 | 17 | 100% |

## 6. 已验证能力

- DRAFT 版本可发布。
- 发布前执行配置校验。
- 发布后 status = PUBLISHED。
- 发布后 config_hash 非空。
- 发布后 published_at 非空。
- 发布后 strategy.latest_version_id 更新为发布版本。
- PUBLISHED 版本不可修改。
- PUBLISHED 版本可复制为 DRAFT。
- 前端 PUBLISHED 版本配置页只读。
- 前端 PUBLISHED 版本可触发“复制为新草稿”。

## 7. 本次修复记录

- 新增 strategy_version 发布字段：`config_hash`、`published_at`、`published_by`。
- 新增版本发布服务。
- 新增版本复制为草稿服务。
- 更新版本详情返回发布字段。
- Gateway 新增 publish/copy 版本代理。
- 前端配置页新增发布确认、只读和复制为草稿。
- 新增 Part 3 远程发布验收脚本。

## 8. 剩余风险

- 版本配置 UI 当前仍为 JSON TextArea，后续可增强为表单化配置编辑。
- 策略审计查询 UI 未做。
- 回测真实执行在 Sprint 5 验收。

## 9. 验收结论

状态：通过。

Sprint 2 Part 3 “策略版本发布与不可变收口”已满足本阶段 P0 验收标准。
