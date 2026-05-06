import {
  ApiOutlined,
  AuditOutlined,
  BellOutlined,
  RobotOutlined,
  SafetyOutlined,
  SettingOutlined,
  TeamOutlined,
  UserSwitchOutlined,
} from '@ant-design/icons';

import { MetricCard } from '@/components/data-display/MetricCard';
import { SectionCard } from '@/components/data-display/SectionCard';
import { PageContainer } from '@/layouts/PageContainer/PageContainer';

import styles from './SystemSettingsPage.module.css';

const modules = [
  { icon: <ApiOutlined />, title: '交易所配置', desc: 'OKX API、模拟盘、行情与权限检测', status: 'OKX 正常' },
  { icon: <RobotOutlined />, title: 'AI模型配置', desc: '复盘、参数优化、反方审查模型', status: '3 个启用' },
  { icon: <SafetyOutlined />, title: '风控参数', desc: '最大回撤、连续亏损、资金费率过滤', status: '12 条生效' },
  { icon: <AuditOutlined />, title: '审计日志', desc: '关键操作、AI调用、配置变更追踪', status: '今日 286 条' },
  { icon: <TeamOutlined />, title: '用户管理', desc: '团队成员、账号状态、最近登录', status: '预留' },
  { icon: <UserSwitchOutlined />, title: '角色权限', desc: '菜单权限、操作权限、数据权限', status: '预留' },
  { icon: <BellOutlined />, title: '通知设置', desc: '回测完成、风险预警、AI复盘通知', status: '预留' },
  { icon: <SettingOutlined />, title: '工作区设置', desc: '工作区信息、默认交易所与主题', status: '默认工作区' },
];

export function SystemSettingsPage() {
  return (
    <PageContainer title="系统设置" description="管理交易所连接、AI模型、风控规则、权限与审计能力。">
      <div className="metric-grid">
        <MetricCard title="交易所连接" value="OKX 正常" trend="模拟盘可用" status="success" />
        <MetricCard title="AI模型" value="3" suffix="个启用" trend="默认 AstraQuant-Insight-XL" status="info" />
        <MetricCard title="风控规则" value="12" suffix="条生效" trend="风控优先级最高" status="success" />
        <MetricCard title="审计日志" value="286" suffix="条" trend="今日操作记录" status="warning" />
      </div>

      <div className={styles.layout}>
        <SectionCard title="设置模块">
          <div className={styles.modules}>
            {modules.map((item) => (
              <div className={styles.moduleCard} key={item.title}>
                <div className={styles.moduleIcon}>{item.icon}</div>
                <div>
                  <strong>{item.title}</strong>
                  <p>{item.desc}</p>
                  <span>{item.status}</span>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="系统健康">
          <div className={styles.healthList}>
            <p>
              <span>当前工作区</span>
              <strong>默认工作区</strong>
            </p>
            <p>
              <span>默认交易所</span>
              <strong>OKX</strong>
            </p>
            <p>
              <span>默认AI模型</span>
              <strong>AstraQuant-Insight-XL</strong>
            </p>
            <p>
              <span>最近AI调用</span>
              <strong>42 次</strong>
            </p>
            <p>
              <span>最近异常告警</span>
              <strong className="text-warning">2 条</strong>
            </p>
          </div>
        </SectionCard>
      </div>
    </PageContainer>
  );
}
