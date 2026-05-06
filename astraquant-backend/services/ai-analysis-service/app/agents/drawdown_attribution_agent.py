from app.agents.base_agent import BaseAgent

class DrawdownAttributionAgent(BaseAgent):
    agent_name = "drawdown_attribution_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "最大回撤主要来自假突破或连续亏损，需要通过回放事件复核", "evidence": ['回撤区间交易亏损集中', '连续亏损会放大回撤'], "risk_level": "HIGH", "suggestions": [{'type': 'PARAMETER_CHANGE', 'content': '提高突破确认时间', 'target_param': 'breakout_confirm_minutes', 'new_value': 3, 'need_retest': True}], "confidence": 0.84}
