from app.agents.base_agent import BaseAgent

class OpponentReviewerAgent(BaseAgent):
    agent_name = "opponent_reviewer_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "当前分析有数据支撑，但缺少样本外验证，需警惕过拟合", "evidence": ['参数优化建议需要重新回测', '未看到样本外回测结果'], "risk_level": "MEDIUM", "suggestions": [{'type': 'VALIDATION_REQUIRED', 'content': '执行样本外回测', 'need_retest': True}], "confidence": 0.84, "detected_issues": [{"issue_type": "OUT_OF_SAMPLE_MISSING", "content": "缺少样本外验证"}]}
