# Sprint 2 最终验收报告：Strategy Service 策略中心

验收时间：2026-05-07T06:44:25Z

## 1. 验收范围

Sprint 2 当前按三部分完成：

```text
Part 1：策略主体与模板
Part 2：策略版本与配置校验
Part 3：策略版本发布与不可变收口
```

真实验收环境：

```text
http://47.239.90.234
```

## 2. 当前已部署服务

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-strategy-service staging-strategy-service Up
astraquant-nats nats:latest Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up (healthy)
```

## 3. Part 1 验收结论

报告：

```text
docs/acceptance/reports/sprint2-part1-strategy-core-report-2026-05-07.md
```

结果：

```text
状态：通过
P0 远程 API 用例：12/12
```

已验证：

- 策略模板可查询。
- 策略可创建。
- 策略 code 唯一约束生效。
- 策略列表可查询。
- 策略详情可查询。
- 策略基础信息可更新。
- 策略可复制。
- 策略可归档。
- 前端策略列表/详情接入真实 API。

## 4. Part 2 验收结论

报告：

```text
docs/acceptance/reports/sprint2-part2-strategy-version-report-2026-05-07.md
```

结果：

```text
状态：通过
P0 远程版本用例：9/9
```

已验证：

- 策略版本列表可查询。
- 策略版本详情可查询。
- 可创建新草稿版本。
- 无 `source_version_id` 时自动选择默认来源。
- 可更新 DRAFT 版本配置。
- 合法配置保存成功。
- 非法 symbols 被拒绝。
- 非法 risk_config 被拒绝。
- 前端版本配置页可编辑 params/risk JSON。

## 5. Part 3 验收结论

报告：

```text
docs/acceptance/reports/sprint2-part3-strategy-publish-report-2026-05-07.md
```

结果：

```text
状态：通过
P0 远程发布用例：11/11
```

已验证：

- DRAFT 版本可发布。
- 发布前执行配置校验。
- 发布后状态为 PUBLISHED。
- 发布后生成 config_hash。
- 发布后写入 published_at / published_by。
- 发布后更新 strategy.latest_version_id。
- PUBLISHED 版本不可修改。
- PUBLISHED 版本可复制为 DRAFT。
- 前端发布版本后进入只读状态。
- 前端支持复制已发布版本为新草稿。

## 6. 当前实现与原始 V1.0 文档差异

| 原始设计 | 当前实现 | 处理 |
|---|---|---|
| APISIX Gateway | FastAPI API Gateway | 保留，沿用 Sprint 1 演进结果 |
| 单用户管理员模式 | RBAC + admin 通配权限 | 保留，admin 可完整使用策略中心 |
| 复杂表单化策略配置 | JSON TextArea + 后端校验 | 先保留，后续增强 UI |
| 完整 Audit Center | Strategy 轻量审计表 + 后续 Sprint 19 Audit Center | 当前 Sprint 满足轻量审计 |
| 回测执行 | 仅提交/配置，不执行回测 | 符合 Sprint 2 范围，Sprint 5 验收 |

## 7. 测试指标汇总

| 测试项 | 结果 |
|---|---:|
| Strategy Service pytest | 8 passed |
| API Gateway pytest | 9 passed |
| Part 1 远程验收 | 12/12 passed |
| Part 2 远程验收 | 9/9 passed |
| Part 3 远程验收 | 11/11 passed |
| 前端策略列表浏览器检查 | passed |
| 前端版本配置浏览器检查 | passed |
| 前端发布版本只读浏览器检查 | passed |

## 8. 剩余风险

- 策略配置 UI 当前为 JSON TextArea，后续可增强为结构化表单组件。
- 策略审计查询 UI 未做。
- 真实回测执行在 Sprint 5 验收。
- 与后续 Signal Engine 的策略配置解释器仍需在 Sprint 11 验收。

## 9. 最终验收结论

状态：通过。

Sprint 2 “Strategy Service 策略中心”已满足当前验收口径：

```text
策略模板可查看；
策略主体可管理；
策略可复制和归档；
策略版本可创建；
策略配置可校验和编辑；
策略版本可发布；
发布版本不可修改；
已发布版本可复制为新草稿；
前端策略中心可真实使用；
真实服务器地址验收通过。
```

可以进入 Sprint 3：Exchange Access Gateway 验收完善。
