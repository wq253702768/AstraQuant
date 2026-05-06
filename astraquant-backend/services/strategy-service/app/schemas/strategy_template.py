from pydantic import BaseModel

class StrategyTemplateListItem(BaseModel):
    id: str
    code: str
    name: str
    strategy_type: str
    description: str | None = None

class StrategyTemplateDetail(StrategyTemplateListItem):
    default_params: dict
    param_schema: dict
    risk_schema: dict
