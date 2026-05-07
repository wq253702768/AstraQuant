# Sprint 4 Part 1 测试报告：K线同步基础链路

测试时间：2026-05-07T12:41:58Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint4-market-data-p1-45f5` |
| 部署提交 | `b2c94ee` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Market Data Service | `http://47.239.90.234/api/market-data/*` |

服务状态：

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-market-data-service staging-market-data-service Up
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
| Market Data Service pytest | 10 passed |
| API Gateway pytest | 10 passed |
| Sprint 4 deploy script syntax | passed |
| Sprint 4 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint4_part1_market_candles.sh
```

结果：

```text
[PASS] login
[PASS] market data health
[PASS] market data rejects missing token
[PASS] create candle sync task
[PASS] run candle sync task
[PASS] query sync task detail
[PASS] query stored candles
[PASS] stored candles count > 0 (72)
[PASS] rerun candle sync task idempotently
```

Sprint 3 交易所访问回归：

```text
12/12 passed
```

## 4. 前端浏览器级验收

使用 headless Chrome 打开真实地址：

```text
http://47.239.90.234/market-data
```

验证结果：

```text
FRONTEND_MARKET_DATA_CANDLE_CHECK_PASS
```

关键断言：

```text
h1 = 历史行情
页面包含 Market Data Service
页面包含 本地 K线数据
K线表格 rows > 0
真实请求 /api/market-data/klines
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 API 用例 | 9 | 9 | 100% |
| P0 前端浏览器用例 | 5 | 5 | 100% |
| 回归自动化测试 | 20 | 20 | 100% |

## 6. 已验证能力

- Market Data Service 可启动。
- Market Data Service health 可访问。
- 无 token 访问 K线接口被拒绝。
- 可创建 K线同步任务。
- 可运行 K线同步任务。
- Market Data Service 通过 Exchange Access Gateway 拉取 K线。
- K线写入 PostgreSQL `market_candle`。
- 可查询本地 K线。
- K线查询结果数量大于 0。
- 同一任务重复运行不会造成接口失败。
- 前端历史行情页可查询本地 K线数据。

## 7. 本次修复记录

- 新增 `market_candle` PostgreSQL 表。
- Market Data Service 使用独立 `alembic_version_market_data` 版本表。
- 新增 PostgreSQL K线 repository。
- 实现 K线同步服务。
- 实现同步任务运行接口。
- 实现同步任务列表接口。
- 实现本地 K线查询接口。
- API Gateway 新增 health、任务列表、任务运行代理。
- 前端新增历史行情页面。
- 新增 Sprint 4 Part 1 staging compose/deploy 脚本。
- 新增 Sprint 4 Part 1 真实地址验收脚本。

## 8. 剩余风险

- 当前 Part 1 只做 K线同步，Funding Rate / Mark Price 同步进入 Part 2。
- 缺口检测、修复、质量报告进入 Part 2 / Part 3。
- 当前同步为接口内同步执行，Celery worker 在后续 Part 3 完善。
- 当前未启用 TimescaleDB hypertable。

## 9. 验收结论

状态：通过。

Sprint 4 Part 1 “K线同步基础链路”已满足本阶段 P0 验收标准，可以进入 Sprint 4 Part 2：资金费率 / 标记价格 / 缺口检测。
