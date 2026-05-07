# Sprint 3 Part 1 测试报告：公共交易所访问基础链路

测试时间：2026-05-07T07:17:42Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint3-exchange-public-p1-45f5` |
| 部署提交 | `03c53b8` |
| Frontend | `http://47.239.90.234` |
| API Gateway | `http://47.239.90.234` |
| Exchange Access Gateway | `http://47.239.90.234/api/exchange-public/*` |
| 首期交易所 | OKX |
| 首期品种 | BTC-USDT-SWAP / ETH-USDT-SWAP |

服务状态：

```text
astraquant-frontend-web staging-frontend-web Up
astraquant-api-gateway staging-api-gateway Up
astraquant-auth-service staging-auth-service Up
astraquant-exchange-access-gateway staging-exchange-access-gateway Up
astraquant-strategy-service staging-strategy-service Up
astraquant-nats nats:latest Up
astraquant-postgres postgres:16 Up (healthy)
astraquant-redis redis:7 Up
```

## 2. 本地自动化测试

| 测试项 | 结果 |
|---|---|
| Exchange Access Gateway go test | passed |
| API Gateway pytest | 10 passed |
| Sprint 3 deploy script syntax | passed |
| Sprint 3 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址 API 验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint3_part1_exchange_public.sh
```

结果：

```text
[PASS] login
[PASS] exchange public rejects missing token
[PASS] exchange public health
[PASS] okx time
[PASS] okx instruments
[PASS] BTC/ETH instruments present
[PASS] okx ticker
[PASS] ticker has last price
[PASS] okx mark price
[PASS] okx funding rate
[PASS] okx klines
[PASS] okx funding history
```

## 4. 前端浏览器级验收

使用 headless Chrome 打开真实地址：

```text
http://47.239.90.234/system-settings/exchange
```

验证结果：

```text
FRONTEND_EXCHANGE_PAGE_CHECK_PASS
```

关键断言：

```text
h1 = 交易所配置
页面包含 Exchange Gateway
页面包含 BTC-USDT-SWAP
页面包含 ETH-USDT-SWAP
合约表格 rows >= 2
真实请求：
  GET /api/exchange-public/health
  GET /api/exchange-public/exchanges/OKX/time
  GET /api/exchange-public/exchanges/OKX/instruments
  GET /api/exchange-public/exchanges/OKX/ticker
  GET /api/exchange-public/exchanges/OKX/mark-price
  GET /api/exchange-public/exchanges/OKX/funding-rate
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 API/Gateway 用例 | 12 | 12 | 100% |
| P0 前端浏览器用例 | 5 | 5 | 100% |
| Go/Gateway 自动化测试 | 10+ | 10+ | 100% |

## 6. 已验证能力

- Exchange Access Gateway 可启动。
- Gateway 可代理 `/api/exchange-public/*`。
- 无 token 访问交易所公共接口被拒绝。
- admin token 可访问交易所公共接口。
- OKX server time 可查询。
- OKX instruments 可查询。
- BTC/ETH SWAP 合约存在。
- BTC ticker 可查询。
- BTC mark price 可查询。
- BTC funding rate 可查询。
- BTC 5m K线可查询。
- BTC funding rate history 可查询。
- 前端交易所配置页展示真实公共数据。

## 7. 本次修复记录

- Exchange Access Gateway 新增 ticker 模型、mapper、adapter、service、handler 和路由。
- API Gateway 新增 Exchange Public Client 与 `/api/exchange-public/*` 代理。
- 前端交易所配置页从静态展示切换为真实公共数据。
- 新增 Sprint 3 最小 staging compose/deploy 脚本。
- 新增 Sprint 3 真实地址验收脚本。
- 修复验收脚本 query string 转义导致 OKX K线 `Parameter bar error` 的问题。

## 8. 剩余风险

- PostgreSQL 合约元数据落库、symbol_mapping 和 Redis 缓存放到 Sprint 3 Part 2。
- Open Interest、限流精细化和错误码最终收口放到 Sprint 3 Part 3。
- OKX 公共 API 可能受网络波动影响，后续需要更细的错误分类和重试策略。

## 9. 验收结论

状态：通过。

Sprint 3 Part 1 “公共交易所访问基础链路”已满足本阶段 P0 验收标准，可以进入 Sprint 3 Part 2：合约元数据、Symbol 映射、K线与资金费率历史增强。
