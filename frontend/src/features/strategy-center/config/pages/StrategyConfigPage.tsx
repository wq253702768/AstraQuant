import { Button, Col, Form, Input, InputNumber, Row, Select, Space } from 'antd';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';
import { StatusTag } from '@/components/status/StatusTag';
import { strategyVersions } from '../../services/mockData';
import type { StrategyVersion } from '../../types';
import styles from './StrategyConfigPage.module.css';

export function StrategyConfigPage() {
  const currentVersion = strategyVersions[0];

  return (
    <PageContainer
      title="策略配置"
      description="管理策略基础信息、交易配置、策略参数、风控参数和委托模型。"
      extra={
        <Space>
          <Button>保存策略</Button>
          <Button type="primary" ghost>
            保存为新版本
          </Button>
          <Button type="primary">开始回测</Button>
        </Space>
      }
    >
      <div className={styles.layout}>
        <div className={styles.main}>
          <SectionCard title="基础信息">
            <Form layout="vertical">
              <Row gutter={16}>
                <Col span={8}>
                  <Form.Item label="策略名称">
                    <Input defaultValue="BTC 趋势突破策略" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="版本">
                    <Input value="v1.3.2" readOnly />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="策略类型">
                    <Select defaultValue="趋势突破" options={[{ value: '趋势突破' }, { value: '均值回归' }]} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="交易方向">
                    <Select defaultValue="双向" options={[{ value: '双向' }, { value: '做多' }, { value: '做空' }]} />
                  </Form.Item>
                </Col>
                <Col span={16}>
                  <Form.Item label="标签">
                    <Select
                      mode="tags"
                      defaultValue={['趋势', '突破']}
                      options={[{ value: '趋势' }, { value: '突破' }, { value: '高波动' }]}
                    />
                  </Form.Item>
                </Col>
              </Row>
            </Form>
          </SectionCard>

          <SectionCard title="交易配置">
            <Form layout="vertical">
              <Row gutter={16}>
                <Col span={8}>
                  <Form.Item label="交易所">
                    <Select defaultValue="OKX" options={[{ value: 'OKX' }]} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="合约">
                    <Select defaultValue="BTC-USDT-SWAP" options={[{ value: 'BTC-USDT-SWAP' }, { value: 'ETH-USDT-SWAP' }]} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="周期">
                    <Select defaultValue="15m" options={[{ value: '5m' }, { value: '15m' }, { value: '1h' }]} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="保证金模式">
                    <Select defaultValue="全仓" options={[{ value: '全仓' }, { value: '逐仓' }]} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="默认杠杆">
                    <Select defaultValue="10x" options={[{ value: '3x' }, { value: '6x' }, { value: '10x' }]} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="初始资金">
                    <InputNumber defaultValue={100000} addonAfter="USDT" style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>
            </Form>
          </SectionCard>

          <SectionCard title="参数设置">
            <Row gutter={16}>
              {[
                ['突破确认', '3', '根K线'],
                ['止损', '1.2', '%'],
                ['止盈', '2.8', '%'],
                ['最大连续亏损', '6', '笔'],
                ['最大回撤阈值', '18', '%'],
              ].map(([label, value, unit]) => (
                <Col span={8} key={label}>
                  <Form layout="vertical">
                    <Form.Item label={label}>
                      <InputNumber defaultValue={Number(value)} addonAfter={unit} style={{ width: '100%' }} />
                    </Form.Item>
                  </Form>
                </Col>
              ))}
              <Col span={8}>
                <Form layout="vertical">
                  <Form.Item label="资金费率过滤">
                    <Select defaultValue="已开启" options={[{ value: '已开启' }, { value: '已关闭' }]} />
                  </Form.Item>
                </Form>
              </Col>
            </Row>
          </SectionCard>

          <SectionCard title="委托模型">
            <Row gutter={16}>
              {[
                ['开仓', 'IOC限价'],
                ['止盈', '限价 reduceOnly'],
                ['止损', 'IOC reduceOnly'],
                ['紧急止损', '市价 reduceOnly'],
              ].map(([label, value]) => (
                <Col span={6} key={label}>
                  <Form layout="vertical">
                    <Form.Item label={label}>
                      <Select defaultValue={value} options={[{ value }]} />
                    </Form.Item>
                  </Form>
                </Col>
              ))}
            </Row>
          </SectionCard>

          <div className={styles.notice}>
            <b>风险提示</b>
            <p>该策略基于历史数据回测，不代表未来收益；策略参数、委托模型和风控变更应保存为新版本后重新回测。</p>
          </div>
        </div>

        <div className={styles.side}>
          <SectionCard title="当前版本信息">
            <div className={styles.infoList}>
              <span>创建时间</span>
              <b>2024-05-01 12:23:36</b>
              <span>创建人</span>
              <b>量化研究员</b>
              <span>状态</span>
              <StatusTag status={currentVersion.status} />
              <span>Code Hash</span>
              <b>{currentVersion.codeHash}</b>
              <span>适用品种</span>
              <b>BTC</b>
            </div>
          </SectionCard>
          <SectionCard title="版本历史">
            {strategyVersions.slice(0, 3).map((version: StrategyVersion) => (
              <div className={styles.versionRow} key={version.id}>
                <b>{version.version}</b>
                <span>{version.createdAt}</span>
                <StatusTag status={version.status} />
              </div>
            ))}
          </SectionCard>
          <SectionCard title="版本差异摘要">
            <div className={styles.diffRow}>
              <span>突破确认</span>
              <b>2根K线 → 3根K线</b>
            </div>
            <div className={styles.diffRow}>
              <span>杠杆</span>
              <b>12x → 10x</b>
            </div>
            <div className={styles.diffRow}>
              <span>单笔亏损</span>
              <b>1.5% → 1.2%</b>
            </div>
          </SectionCard>
        </div>
      </div>
    </PageContainer>
  );
}
