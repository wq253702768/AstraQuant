from app.agents.base_agent import BaseAgent

class CostAnalyzerAgent(BaseAgent):
    agent_name = "cost_analyzer_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "交易成本会侵蚀净利润，需要控制交易频率和滑点", "evidence": ['手续费、滑点、资金费均已纳入成本摘要'], "risk_level": "MEDIUM", "suggestions": [{'type': 'ORDER_EXECUTION_CHANGE', 'content': '低波动阶段优先测试限价执行', 'need_retest': True}], "confidence": 0.84}
