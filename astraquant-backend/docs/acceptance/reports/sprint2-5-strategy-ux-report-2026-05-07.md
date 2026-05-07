# Sprint 2.5 测试报告：策略中心 UX 安全补强

测试时间：2026-05-07T12:05:12Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint2-5-strategy-ux-45f5` |
| 部署提交 | `22ca94f` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Strategy Service | `http://47.239.90.234/api/strategies*` |

服务状态：

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-strategy-service staging-strategy-service Up
astraquant-exchange-access-gateway staging-exchange-access-gateway Up
astraquant-nats nats:latest Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up
```

## 2. 本地自动化测试

| 测试项 | 结果 |
|---|---|
| Exchange Access Gateway go test | passed |
| API Gateway pytest | 10 passed |
| Sprint 2.5 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器 API 验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint2_5_strategy_ux.sh
```

结果：

```text
[PASS] login
[PASS] list templates
[PASS] template detail
[PASS] template detail includes default_config/schema
[PASS] create strategy
[PASS] update strategy
[PASS] copy strategy
[PASS] list versions
[PASS] version detail
[PASS] archive strategy
```

## 4. 浏览器级验收

### 4.1 策略模板只读页

验证结果：

```text
策略模板菜单可见
模板列表真实加载
模板详情真实加载
模板详情包含 default_config
模板详情包含 param_schema
模板详情包含 risk_schema
模板详情无编辑/删除按钮
```

### 4.2 新建策略确认框

验证结果：

```text
STRATEGY_CREATE_CONFIRM_CHECK_PASS
```

关键断言：

```text
确认框标题 = 确认创建策略？
确认框文案包含：系统将基于所选模板创建策略，并生成初始草稿版本。
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 API 用例 | 10 | 10 | 100% |
| P0 模板只读用例 | 7 | 7 | 100% |
| P0 确认框用例 | 1 | 1 | 100% |
| 回归自动化测试 | 10+ | 10+ | 100% |

## 6. 已验证能力

- 策略模板菜单入口可见。
- 模板列表页可打开并加载真实 API。
- 模板详情页可打开并展示只读配置。
- 模板详情页没有编辑/删除操作。
- 新建策略提交前出现确认框。
- API 层策略创建、更新、复制、归档能力仍可用。

## 7. 本次修复记录

- 新增策略模板菜单入口。
- 新增策略模板列表页。
- 新增策略模板详情页。
- 新建策略增加确认框。
- 编辑策略基础信息增加确认框。
- 复制策略增加确认框。
- 归档策略增加高风险确认框。
- 新建策略版本增加确认框。
- 保存版本配置增加确认框。
- 复制已发布版本为新草稿增加确认框。
- 优化发布版本确认文案。
- 新增 Sprint 2.5 远程验收脚本。

## 8. 剩余风险

- 自定义模板创建/编辑/停用尚未实现。
- 策略模板版本化尚未实现。
- 复杂策略配置表单化编辑仍未实现。

## 9. 验收结论

状态：通过。

Sprint 2.5 “策略中心 UX 安全补强”已满足本阶段 P0 验收标准。
