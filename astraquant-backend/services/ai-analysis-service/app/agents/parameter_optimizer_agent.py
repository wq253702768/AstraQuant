from app.agents.base_agent import BaseAgent

class ParameterOptimizerAgent(BaseAgent):
    agent_name = "parameter_optimizer_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        return {"agent_name": self.agent_name, "conclusion": "建议优先测试更严格的突破确认和连续亏损冷却参数", "evidence": ['回撤归因指向假突破', '成本分析显示存在过度交易风险'], "risk_level": "MEDIUM", "suggestions": [{'type': 'PARAMETER_SET', 'name': '保守突破过滤方案', 'params_patch': {'breakout_confirm_minutes': 3, 'volume_multiplier': 1.8}, 'risk_params_patch': {'max_consecutive_losses': 3}, 'need_retest': True}], "confidence": 0.84}
