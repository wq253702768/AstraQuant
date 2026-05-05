import { Button, Col, DatePicker, Form, InputNumber, Row, Select, Switch } from 'antd';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';

const { RangePicker } = DatePicker;

export function NewBacktestPage() {
  return (
    <PageContainer
      title="新建回测"
      description="配置回测范围、数据、成本模型与执行参数，创建可复现的回测任务。"
      extra={
        <>
          <Button>保存配置</Button>
          <Button type="primary">开始数据校验</Button>
        </>
      }
    >
      <Row gutter={[16, 16]}>
        <Col span={16}>
          <SectionCard title="回测配置">
            <Form layout="vertical">
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item label="策略">
                    <Select defaultValue="ETH 均值回归 v3" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item label="版本">
                    <Select defaultValue="v3.2.0" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="交易所">
                    <Select defaultValue="OKX" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="合约">
                    <Select defaultValue="ETH-USDT-SWAP" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="周期">
                    <Select defaultValue="1H" />
                  </Form.Item>
                </Col>
                <Col span={24}>
                  <Form.Item label="回测时间范围">
                    <RangePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="初始资金">
                    <InputNumber addonAfter="USDT" defaultValue={100000} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="默认杠杆">
                    <Select defaultValue="10x" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item label="保证金模式">
                    <Select defaultValue="全仓" />
                  </Form.Item>
                </Col>
              </Row>
            </Form>
          </SectionCard>
        </Col>
        <Col span={8}>
          <SectionCard title="成本与执行设置">
            <Form layout="vertical">
              <Form.Item label="Maker 费率">
                <InputNumber addonAfter="%" defaultValue={0.02} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item label="Taker 费率">
                <InputNumber addonAfter="%" defaultValue={0.04} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item label="资金费率">
                <Switch defaultChecked />
              </Form.Item>
              <Form.Item label="生成回撤与回放">
                <Switch defaultChecked />
              </Form.Item>
              <Form.Item label="自动触发 AI 复盘">
                <Switch defaultChecked />
              </Form.Item>
            </Form>
          </SectionCard>
        </Col>
      </Row>
    </PageContainer>
  );
}
