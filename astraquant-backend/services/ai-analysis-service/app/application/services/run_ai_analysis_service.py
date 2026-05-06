from app.domain.enums.ai_task_status import AITaskStatus
from app.domain.services.ai_output_validator import AIOutputValidator
from app.domain.services.input_data_hash_service import InputDataHashService
from app.graph.backtest_review_graph import BacktestReviewGraph
from app.infrastructure.clients.backtest_service_client import BacktestServiceClient
from app.infrastructure.clients.replay_service_client import ReplayServiceClient
from app.infrastructure.postgres.models import AIAgentOutputModel
from app.infrastructure.repositories.ai_agent_output_repository import AIAgentOutputRepository
from app.infrastructure.repositories.ai_task_repository import AITaskRepository
from app.application.services.model_call_log_service import ModelCallLogService

OUTPUT_KEYS = ["data_validation_output", "strategy_performance_output", "drawdown_attribution_output", "cost_analyzer_output", "parameter_optimizer_output", "risk_reviewer_output", "opponent_reviewer_output", "summary_output"]

class RunAIAnalysisService:
    def __init__(self, session):
        self.session = session
        self.task_repo = AITaskRepository(session)
        self.output_repo = AIAgentOutputRepository(session)
        self.validator = AIOutputValidator()
        self.model_logger = ModelCallLogService(session)

    async def run(self, ai_task_id: str):
        task = await self.task_repo.get(ai_task_id)
        if not task: return None
        task.status = AITaskStatus.LOADING_DATA.value
        input_data = await BacktestServiceClient().load_review_input(task.related_task_id)
        input_data["replay_events_sample"] = await ReplayServiceClient().sample_events(task.related_task_id)
        input_hash = InputDataHashService().calculate(input_data)
        task.input_data_hash = input_hash
        task.status = AITaskStatus.RUNNING.value
        state = BacktestReviewGraph().invoke({"ai_task_id": task.id, "backtest_task_id": str(task.related_task_id), "input_data": input_data, "input_data_hash": input_hash, "errors": []})
        task.status = AITaskStatus.VALIDATING_OUTPUT.value
        agent_outputs = []
        for key in OUTPUT_KEYS:
            output = state.get(key)
            if not output: continue
            self.validator.validate(output)
            agent_outputs.append(output)
            await self.output_repo.create(AIAgentOutputModel(ai_task_id=task.id, agent_name=output["agent_name"], conclusion=output.get("conclusion"), evidence_json=output.get("evidence"), suggestions_json=output.get("suggestions"), risk_level=output.get("risk_level"), confidence=output.get("confidence"), output_json=output))
            await self.model_logger.log_mock_call(task.id, output["agent_name"], input_hash, output)
        task.result_json = {"summary": state.get("summary_output"), "agents": agent_outputs}
        task.current_agent = None
        task.progress = 100
        task.status = AITaskStatus.COMPLETED.value
        return task
