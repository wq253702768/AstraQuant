import { Button, Descriptions, Input, Space, Tag } from 'antd';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { PageContainer } from '@/layouts/PageContainer/PageContainer';
import { SectionCard } from '@/components/data-display/SectionCard';
import { strategyApi } from '@/services/strategy.api';
import type { StrategyTemplate } from '@/types/strategy';

function formatJson(value: unknown) {
  return JSON.stringify(value ?? {}, null, 2);
}

export function StrategyTemplateDetailPage() {
  const { templateId } = useParams();
  const navigate = useNavigate();
  const [template, setTemplate] = useState<StrategyTemplate | null>(null);

  useEffect(() => {
    if (templateId) {
      void strategyApi.templateDetail(templateId).then(setTemplate);
    }
  }, [templateId]);

  if (!template) {
    return <PageContainer title="策略模板">加载中...</PageContainer>;
  }

  return (
    <PageContainer
      title={template.name}
      description="策略模板当前为只读。请基于模板创建策略后，在策略版本配置中自定义参数。"
      extra={<Button onClick={() => navigate('/strategy-center/templates')}>返回模板列表</Button>}
    >
      <div className="page-stack">
        <SectionCard title="模板基础信息">
          <Descriptions bordered column={2} size="small">
            <Descriptions.Item label="模板编码">{template.code}</Descriptions.Item>
            <Descriptions.Item label="策略类型">{template.strategy_type}</Descriptions.Item>
            <Descriptions.Item label="状态"><Tag color="green">只读 / 启用</Tag></Descriptions.Item>
            <Descriptions.Item label="说明">{template.description || '-'}</Descriptions.Item>
          </Descriptions>
        </SectionCard>

        <SectionCard title="默认配置 default_config">
          <Input.TextArea readOnly rows={12} value={formatJson(template.default_config ?? template.default_params)} />
        </SectionCard>

        <div className="two-column">
          <SectionCard title="参数 Schema">
            <Input.TextArea readOnly rows={16} value={formatJson(template.param_schema)} />
          </SectionCard>
          <SectionCard title="风险 Schema">
            <Input.TextArea readOnly rows={16} value={formatJson(template.risk_schema)} />
          </SectionCard>
        </div>

        <SectionCard title="操作建议">
          <Space direction="vertical">
            <span>如果要自定义策略，请先返回策略列表，新建策略并选择该模板。</span>
            <span>模板本身不支持直接编辑或删除，避免影响已有策略追溯。</span>
          </Space>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
