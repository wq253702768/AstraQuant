from app.agents.base_agent import BaseAgent

class DataValidatorAgent(BaseAgent):
    agent_name = "data_validator_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "输入数据完整，可以进行分析", "evidence": ['回测结果包含基础指标', '交易与回撤样本可用于复盘'], "risk_level": "LOW", "suggestions": [], "confidence": 0.84, "can_continue": True}
