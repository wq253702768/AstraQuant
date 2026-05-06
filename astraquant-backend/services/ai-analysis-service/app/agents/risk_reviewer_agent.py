from app.agents.base_agent import BaseAgent

class RiskReviewerAgent(BaseAgent):
    agent_name = "risk_reviewer_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "当前策略可进入模拟盘观察，不建议直接进入实盘", "evidence": ['最大回撤和连续亏损需要风控约束', 'AI不替代最终准入判断'], "risk_level": "HIGH", "suggestions": [{'type': 'ADMISSION_RECOMMENDATION', 'content': '允许模拟盘，不允许实盘', 'recommended_decision': 'ALLOW_SIMULATION_NOT_LIVE', 'need_retest': False}], "confidence": 0.84}
