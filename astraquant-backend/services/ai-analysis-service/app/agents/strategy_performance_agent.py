from app.agents.base_agent import BaseAgent

class StrategyPerformanceAgent(BaseAgent):
    agent_name = "strategy_performance_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "策略具备趋势行情盈利能力，但收益稳定性需要继续观察", "evidence": ['总收益率和最大回撤可量化', '胜率和盈亏比可用于评估收益质量'], "risk_level": "MEDIUM", "suggestions": [{'type': 'REVIEW_REQUIRED', 'content': '观察收益是否集中在少数交易', 'need_retest': False}], "confidence": 0.84}
