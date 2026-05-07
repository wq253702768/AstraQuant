# Sprint 3 Part 2 测试报告：合约元数据 / Symbol 映射 / K线与资金费率历史

测试时间：2026-05-07T08:14:37Z

## 1. 测试环境

| 项目 | 值 |
|---|---|
| 分支 | `cursor/sprint3-exchange-public-p1-45f5` |
| 部署提交 | `b957152` |
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
| Sprint 3 Part 2 acceptance script syntax | passed |
| Frontend Docker build | passed |

## 3. 真实服务器地址 API 验收

执行命令：

```bash
ASTRA_GATEWAY_URL=http://47.239.90.234 \
ASTRA_TEST_PASSWORD=password \
scripts/acceptance/sprint3_part2_exchange_metadata.sh
```

结果：

```text
[PASS] login
[PASS] sync instruments
[PASS] query stored instruments
[PASS] stored BTC/ETH instruments present
[PASS] query stored instrument detail
[PASS] query symbol mappings
[PASS] BTC/ETH symbol mappings present
[PASS] valid klines
[PASS] invalid timeframe rejected (BAD_RESPONSE)
[PASS] kline limit rejected (RATE_LIMITED)
[PASS] valid funding history
[PASS] funding history limit rejected (RATE_LIMITED)
```

Part 1 回归：

```text
12/12 passed
```

## 4. 前端浏览器级验收

使用 headless Chrome 打开真实地址：

```text
http://47.239.90.234/system-settings/exchange
```

验证结果：

```text
FRONTEND_EXCHANGE_METADATA_CHECK_PASS
```

关键断言：

```text
h1 = 交易所配置
页面包含 已同步合约规格
页面包含 Symbol 映射
页面包含 K线查询
页面包含 资金费率历史
页面包含 BTC-USDT-SWAP
页面包含 ETH-USDT-SWAP
表格行数 >= 6
```

## 5. 用例通过率

| 类型 | 通过 | 总数 | 通过率 |
|---|---:|---:|---:|
| P0 Part 2 API 用例 | 12 | 12 | 100% |
| P0 Part 1 回归用例 | 12 | 12 | 100% |
| P0 前端浏览器用例 | 7 | 7 | 100% |
| Go/Gateway 自动化测试 | 10+ | 10+ | 100% |

## 6. 已验证能力

- 可同步 OKX SWAP 合约。
- 只保留 BTC/ETH SWAP 合约元数据。
- 可查询已同步合约列表。
- 可查询单个合约详情。
- 可查询 Symbol 映射。
- K线合法查询可返回数据。
- K线非法 timeframe 被拒绝。
- K线 limit 超限被拒绝。
- 资金费率历史合法查询可返回数据。
- 资金费率历史 limit 超限被拒绝。
- 前端展示已同步合约、Symbol 映射、K线和资金费率历史。

## 7. 本次修复记录

- 新增合约元数据同步接口。
- 新增合约元数据内存存储与 Symbol 映射。
- 新增 DB-style instruments 查询接口。
- 新增单个 instrument 查询接口。
- 新增 symbol mappings 查询接口。
- 增强 K线参数校验。
- 增强 funding history 参数校验。
- Gateway 新增 metadata 代理接口。
- 前端交易所配置页增加同步合约、已同步合约、Symbol 映射、K线查询、资金费率历史区块。

## 8. 剩余风险

- 当前合约元数据为服务内存存储，PostgreSQL 持久化可在后续增强。
- Redis 缓存接口尚未真实启用。
- Open Interest、精细限流和最终错误码标准化放到 Sprint 3 Part 3。

## 9. 验收结论

状态：通过。

Sprint 3 Part 2 “合约元数据 / Symbol 映射 / K线与资金费率历史增强”已满足本阶段 P0 验收标准，可以进入 Sprint 3 Part 3。
