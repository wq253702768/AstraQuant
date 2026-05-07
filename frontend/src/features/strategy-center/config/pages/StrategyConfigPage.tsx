import { Button, Form, Input, Modal, Space, Tag, message } from 'antd';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';
import { strategyApi } from '@/services/strategy.api';
import type { StrategyVersionDetail } from '@/types/strategy';
import styles from './StrategyConfigPage.module.css';

interface VersionConfigForm {
  params_json: string;
  risk_params_json: string;
}

function formatJson(value: unknown) {
  return JSON.stringify(value ?? {}, null, 2);
}

function parseJson(value: string, label: string) {
  try {
    return JSON.parse(value || '{}') as Record<string, unknown>;
  } catch {
    throw new Error(`${label} 不是合法 JSON`);
  }
}

export function StrategyConfigPage() {
  const { strategyId, versionId } = useParams();
  const navigate = useNavigate();
  const [version, setVersion] = useState<StrategyVersionDetail | null>(null);
  const [form] = Form.useForm<VersionConfigForm>();

  const load = async () => {
    if (!strategyId) return;
    let targetVersionId = versionId;
    if (!targetVersionId) {
      const versions = await strategyApi.versions(strategyId);
      targetVersionId = versions.items[versions.items.length - 1]?.id;
    }
    if (!targetVersionId) return;
    const result = await strategyApi.versionDetail(strategyId, targetVersionId);
    setVersion(result);
    form.setFieldsValue({
      params_json: formatJson(result.params_json),
      risk_params_json: formatJson(result.risk_params_json),
    });
  };

  useEffect(() => {
    void load();
  }, [strategyId, versionId]);

  const handleSave = async (values: VersionConfigForm) => {
    if (!version) return;
    const params = parseJson(values.params_json, '策略参数');
    const risk = parseJson(values.risk_params_json, '风控参数');
    await strategyApi.updateVersionParams(version.id, {
      params_json: params,
      risk_params_json: risk,
    });
    message.success('策略版本配置已保存');
    await load();
  };

  const handlePublish = async () => {
    if (!strategyId || !version) return;
    Modal.confirm({
      title: '确认发布策略版本？',
      content: '发布后该策略版本将不可修改，后续回测、模拟盘和实盘都将引用该版本配置。',
      okText: '确认发布',
      cancelText: '取消',
      onOk: async () => {
        await strategyApi.publishVersion(strategyId, version.id, '前端确认发布');
        message.success('策略版本已发布');
        await load();
      },
    });
  };

  const handleCopyDraft = async () => {
    if (!strategyId || !version) return;
    const result = await strategyApi.copyVersion(strategyId, version.id, '基于已发布版本复制为新草稿');
    message.success('已复制为新草稿');
    navigate(`/strategy-center/strategies/${strategyId}/versions/${result.strategy_version_id}/config`);
  };

  if (!version) {
    return <PageContainer title="策略配置">加载中...</PageContainer>;
  }

  const editable = version.status === 'DRAFT';

  return (
    <PageContainer
      title={`策略配置 ${version.version}`}
      description="编辑草稿策略版本的参数 JSON 与风控 JSON。已发布版本只允许查看。"
      extra={
        <Space>
          <Tag color={editable ? 'blue' : 'default'}>{version.status}</Tag>
          {editable ? <Button type="primary" onClick={handlePublish}>发布版本</Button> : <Button onClick={handleCopyDraft}>复制为新草稿</Button>}
          <Button onClick={() => navigate(`/strategy-center/strategies/${strategyId}`)}>返回策略详情</Button>
        </Space>
      }
    >
      <div className={styles.layout}>
        <div className={styles.main}>
          <SectionCard title="版本配置">
            <Form form={form} layout="vertical" onFinish={handleSave}>
              <Form.Item label="策略参数 params_json" name="params_json" rules={[{ required: true, message: '请输入策略参数 JSON' }]}>
                <Input.TextArea rows={18} readOnly={!editable} />
              </Form.Item>
              <Form.Item label="风控参数 risk_params_json" name="risk_params_json" rules={[{ required: true, message: '请输入风控参数 JSON' }]}>
                <Input.TextArea rows={12} readOnly={!editable} />
              </Form.Item>
              <Button type="primary" htmlType="submit" disabled={!editable}>
                保存配置
              </Button>
            </Form>
          </SectionCard>
        </div>
        <div className={styles.side}>
          <SectionCard title="版本信息">
            <div className={styles.infoList}>
              <span>版本号</span>
              <b>{version.version}</b>
              <span>状态</span>
              <b>{version.status}</b>
              <span>参数 Hash</span>
              <b>{version.params_hash}</b>
              <span>配置 Hash</span>
              <b>{version.config_hash || '-'}</b>
              <span>发布时间</span>
              <b>{version.published_at || '-'}</b>
              <span>来源版本</span>
              <b>{version.source_version_id || '-'}</b>
            </div>
          </SectionCard>
          <div className={styles.notice}>
            <b>配置校验说明</b>
            <p>保存时后端会校验交易品种、周期、指标类型、开仓/平仓规则和风控参数。</p>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
