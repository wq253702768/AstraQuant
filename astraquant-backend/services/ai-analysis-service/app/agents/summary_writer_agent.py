from app.agents.base_agent import BaseAgent

class SummaryWriterAgent(BaseAgent):
    agent_name = "summary_writer_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "策略具备一定趋势捕捉能力，但假突破、成本和样本外缺失是主要风险，建议优化后重新回测。", "evidence": ['收益、回撤、成本和反方审查均给出证据', '所有参数建议均需重新回测'], "risk_level": "MEDIUM", "suggestions": [{'type': 'NEXT_ACTION', 'content': '创建新策略版本并执行样本外回测', 'need_retest': True}], "confidence": 0.84, "final_recommendation": "RETEST_REQUIRED", "key_findings": ["收益来自趋势行情", "回撤来自假突破", "缺少样本外验证"]}
