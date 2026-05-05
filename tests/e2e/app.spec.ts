import { expect, test, type Page } from '@playwright/test';

const demoStrategyId = 'str_btc_breakout';
const demoTaskId = 'demo-task';

async function login(page: Page) {
  await page.goto('/auth/login');
  await expect(page.getByRole('heading', { name: '登录工作台' })).toBeVisible();
  await page.getByLabel('邮箱 / 用户名').fill('quant@astraquant.ai');
  await page.getByLabel('密码').fill('demo-password');
  await page.getByTestId('login-submit').click();
  await expect(page).toHaveURL(/\/dashboard$/);
  await expect(page.getByRole('heading', { name: '总览大盘' })).toBeVisible();
}

test.describe('认证与应用壳', () => {
  test('未登录访问根路径会跳转登录页，登录后进入总览', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/auth\/login$/);
    await expect(page.getByText('AstraQuant 星枢量化')).toBeVisible();
    await expect(page.getByText('AI 驱动的加密货币永续合约智能交易系统')).toBeVisible();

    await page.getByTestId('login-submit').click();
    await expect(page.getByText('请输入账号')).toBeVisible();
    await expect(page.getByText('请输入密码')).toBeVisible();

    await page.getByLabel('工作区').click();
    await expect(page.getByText('默认工作区').last()).toBeVisible();
    await page.keyboard.press('Escape');
    await page.getByRole('checkbox', { name: '记住登录' }).check();
    await expect(page.getByRole('checkbox', { name: '记住登录' })).toBeChecked();

    await page.getByLabel('邮箱 / 用户名').fill('quant@astraquant.ai');
    await page.getByLabel('密码').fill('demo-password');
    await page.getByRole('button', { name: 'SSO 登录' }).click();
    await expect(page.getByRole('heading', { name: '登录工作台' })).toBeVisible();
    await page.getByTestId('login-submit').click();
    await expect(page).toHaveURL(/\/dashboard$/);
  });

  test('主布局包含导航、顶部搜索、工作区、通知和用户信息', async ({ page }) => {
    await login(page);
    await expect(page.getByText('AstraQuant', { exact: true })).toBeVisible();
    await expect(page.getByPlaceholder('搜索策略、合约、指标...')).toBeVisible();
    await expect(page.getByText('默认工作区')).toBeVisible();
    await expect(page.getByText('张三')).toBeVisible();
    await expect(page.getByText('策略中心')).toBeVisible();
    await expect(page.getByText('系统设置')).toBeVisible();
  });
});

test.describe('总览大盘', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('展示总览核心指标、图表与策略状态表', async ({ page }) => {
    await expect(page.getByText('策略总数')).toBeVisible();
    await expect(page.getByText('可进入模拟盘')).toBeVisible();
    await expect(page.getByText('AI复盘任务')).toBeVisible();
    await expect(page.getByText('系统连接', { exact: true })).toBeVisible();
    await expect(page.getByText('策略池净值概览')).toBeVisible();
    await expect(page.getByText('策略运行状态')).toBeVisible();
    await expect(page.getByText('ETH 均值回归 v3')).toBeVisible();
    await expect(page.getByText('近期任务')).toBeVisible();
  });
});

test.describe('策略中心路由、页面与交互', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('策略中心全部菜单路由可访问', async ({ page }) => {
    const pages = [
      ['/strategy-center/strategies', '策略列表'],
      [`/strategy-center/strategies/${demoStrategyId}`, 'BTC 趋势突破策略'],
      [`/strategy-center/strategies/${demoStrategyId}/config`, '策略配置'],
      [`/strategy-center/strategies/${demoStrategyId}/versions`, '策略版本'],
      ['/strategy-center/backtests/new', '新建回测'],
      [`/strategy-center/backtests/${demoTaskId}/validation`, '数据校验'],
      [`/strategy-center/backtests/${demoTaskId}/execution`, '回测执行'],
      [`/strategy-center/backtests/${demoTaskId}/result`, '回测结果'],
      [`/strategy-center/backtests/${demoTaskId}/trades`, '交易明细'],
      [`/strategy-center/backtests/${demoTaskId}/costs`, '成本分析'],
      [`/strategy-center/backtests/${demoTaskId}/drawdowns`, '策略回撤'],
      [`/strategy-center/backtests/${demoTaskId}/replay`, '回撤回放'],
      [`/strategy-center/backtests/${demoTaskId}/ai-review`, 'AI策略复盘'],
      [`/strategy-center/backtests/${demoTaskId}/optimization`, '参数优化'],
      [`/strategy-center/backtests/${demoTaskId}/score`, '策略评分'],
      [`/strategy-center/backtests/${demoTaskId}/report`, '回测报告'],
      ['/strategy-center/paper-validation', '模拟盘验证'],
    ] as const;

    for (const [url, heading] of pages) {
      await page.goto(url);
      await expect(page.getByRole('heading', { name: heading, exact: true })).toBeVisible();
      await expect(page.locator('body')).not.toContainText('404');
    }
  });

  test('策略列表支持搜索、筛选和行内跳转', async ({ page }) => {
    await page.goto('/strategy-center/strategies');
    await page.getByPlaceholder('搜索策略名 / 标签 / 合约').fill('BTC');
    await expect(page.getByText('趋势突破', { exact: true })).toBeVisible();
    await expect(page.getByText('允许模拟盘').first()).toBeVisible();

    await expect(page.getByText('BTC 趋势突破策略')).toBeVisible();
    await page.getByRole('button', { name: '查看' }).first().click();
    await expect(page).toHaveURL(/\/strategy-center\/strategies\/str_/);
    await expect(page.getByText('模拟盘准入：允许')).toBeVisible();

    await page.goto('/strategy-center/strategies');
    await page.getByRole('button', { name: '配置' }).first().click();
    await expect(page).toHaveURL(/\/config$/);

    await page.goto('/strategy-center/strategies');
    await page.getByRole('button', { name: '回测', exact: true }).first().click();
    await expect(page).toHaveURL(/\/strategy-center\/backtests\/new$/);
  });

  test('策略配置表单、版本信息和风险提示可操作可见', async ({ page }) => {
    await page.goto(`/strategy-center/strategies/${demoStrategyId}/config`);
    await expect(page.getByRole('button', { name: '保存策略' })).toBeVisible();
    await expect(page.getByRole('button', { name: '保存为新版本' })).toBeVisible();
    await expect(page.getByRole('button', { name: '开始回测' })).toBeVisible();

    await page.getByTestId('strategy-name-input').fill('BTC 趋势突破策略 Pro');
    await expect(page.getByText('策略类型')).toBeVisible();
    await expect(page.getByText('交易方向')).toBeVisible();
    await expect(page.getByText('BTC-USDT-SWAP')).toBeVisible();
    await page.locator('input[role="spinbutton"]').first().fill('4');

    await expect(page.getByText('该策略基于历史数据回测，不代表未来收益')).toBeVisible();
    await expect(page.getByText('当前版本信息')).toBeVisible();
    await expect(page.getByText('Code Hash')).toBeVisible();
    await expect(page.getByText('版本差异摘要')).toBeVisible();
  });

  test('新建回测页面展示配置、成本模型、校验和风险提示', async ({ page }) => {
    await page.goto('/strategy-center/backtests/new');
    await expect(page.getByText('策略与版本')).toBeVisible();
    await expect(page.getByText('回测市场')).toBeVisible();
    await expect(page.getByRole('heading', { name: '成本模型' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '数据校验设置' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '配置摘要' })).toBeVisible();
    await expect(page.getByText('回测通过不等于可直接实盘')).toBeVisible();
    await page.getByRole('button', { name: '开始数据校验' }).click();
    await expect(page.getByRole('heading', { name: '新建回测' })).toBeVisible();
  });

  test('分析类页面包含任务状态、审计状态和数据预览', async ({ page }) => {
    const urls = [
      `/strategy-center/backtests/${demoTaskId}/validation`,
      `/strategy-center/backtests/${demoTaskId}/execution`,
      `/strategy-center/backtests/${demoTaskId}/result`,
      `/strategy-center/backtests/${demoTaskId}/trades`,
      `/strategy-center/backtests/${demoTaskId}/costs`,
      `/strategy-center/backtests/${demoTaskId}/drawdowns`,
      `/strategy-center/backtests/${demoTaskId}/replay`,
      `/strategy-center/backtests/${demoTaskId}/ai-review`,
      `/strategy-center/backtests/${demoTaskId}/optimization`,
      `/strategy-center/backtests/${demoTaskId}/score`,
      `/strategy-center/backtests/${demoTaskId}/report`,
      '/strategy-center/paper-validation',
    ];

    for (const url of urls) {
      await page.goto(url);
      await expect(page.getByText('运行正常')).toBeVisible();
      await expect(page.getByText('v1.3.2', { exact: true }).first()).toBeVisible();
      await expect(page.getByText('已记录')).toBeVisible();
      await expect(page.getByText('数据预览')).toBeVisible();
      await page.getByRole('button', { name: '导出报告' }).click();
    }
  });
});

test.describe('系统设置页面与安全约束', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('系统设置全部路由可访问', async ({ page }) => {
    const pages = [
      ['/system-settings', '系统设置'],
      ['/system-settings/exchange', '交易所配置'],
      ['/system-settings/ai-models', 'AI模型配置'],
      ['/system-settings/risk', '风控参数'],
      ['/system-settings/audit-logs', '审计日志'],
      ['/system-settings/users', '用户管理'],
      ['/system-settings/roles', '角色权限'],
      ['/system-settings/notifications', '通知设置'],
    ] as const;

    for (const [url, heading] of pages) {
      await page.goto(url);
      await expect(page.getByRole('heading', { name: heading })).toBeVisible();
    }
  });

  test('设置首页模块入口、交易所安全提示和 AI 安全约束正确', async ({ page }) => {
    await page.goto('/system-settings');
    await expect(page.getByText('交易所连接', { exact: true })).toBeVisible();
    await expect(page.getByText('AI模型', { exact: true })).toBeVisible();
    await expect(page.getByText('AI 不可下单')).toBeVisible();

    await page.goto('/system-settings/exchange');
    await expect(page.getByRole('heading', { name: 'OKX 配置详情' })).toBeVisible();
    await expect(page.getByText('实盘交易关闭 · 提币权限禁止')).toBeVisible();
    await expect(page.getByText('第一阶段建议仅启用只读和模拟盘权限')).toBeVisible();
    await page.getByRole('button', { name: '连接测试' }).click();

    await page.goto('/system-settings/ai-models');
    await expect(page.getByText('是否可下单')).toBeVisible();
    await expect(page.getByText('是否可修改策略')).toBeVisible();
    await expect(page.getByText('是否进入交易热路径')).toBeVisible();
    await expect(page.getByText('否').first()).toBeVisible();
    await page.getByRole('button', { name: '连接测试' }).click();
  });

  test('审计日志筛选、表格和导出交互可用', async ({ page }) => {
    await page.goto('/system-settings/audit-logs');
    await expect(page.getByText('今日操作')).toBeVisible();
    await expect(page.getByText('AI调用', { exact: true })).toBeVisible();
    await expect(page.getByText('策略版本变更')).toBeVisible();
    await page.getByPlaceholder('搜索审计ID / 关键词').fill('rev_');
    await page.getByRole('button', { name: '导出日志' }).click();
    await expect(page.getByText('审计ID')).toBeVisible();
  });
});

