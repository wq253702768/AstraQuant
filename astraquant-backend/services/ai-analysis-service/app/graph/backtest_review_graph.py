from app.agents.cost_analyzer_agent import CostAnalyzerAgent
from app.agents.data_validator_agent import DataValidatorAgent
from app.agents.drawdown_attribution_agent import DrawdownAttributionAgent
from app.agents.opponent_reviewer_agent import OpponentReviewerAgent
from app.agents.parameter_optimizer_agent import ParameterOptimizerAgent
from app.agents.risk_reviewer_agent import RiskReviewerAgent
from app.agents.strategy_performance_agent import StrategyPerformanceAgent
from app.agents.summary_writer_agent import SummaryWriterAgent

class BacktestReviewGraph:
    steps = [
        ("data_validation_output", DataValidatorAgent()),
        ("strategy_performance_output", StrategyPerformanceAgent()),
        ("drawdown_attribution_output", DrawdownAttributionAgent()),
        ("cost_analyzer_output", CostAnalyzerAgent()),
        ("parameter_optimizer_output", ParameterOptimizerAgent()),
        ("risk_reviewer_output", RiskReviewerAgent()),
        ("opponent_reviewer_output", OpponentReviewerAgent()),
        ("summary_output", SummaryWriterAgent()),
    ]
    def invoke(self, state: dict) -> dict:
        previous = {}
        for key, agent in self.steps:
            if key != "summary_output" and state.get("data_validation_output", {}).get("can_continue") is False:
                continue
            output = agent.run(state.get("input_data", {}), previous)
            state[key] = output
            previous[key] = output
        return state
