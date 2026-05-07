from pydantic import BaseModel

class StrategyTemplateListItem(BaseModel):
    id: str
    code: str
    name: str
    strategy_type: str
    description: str | None = None
    default_config: dict | None = None

class StrategyTemplateDetail(StrategyTemplateListItem):
    default_params: dict
    default_config: dict | None = None
    param_schema: dict
    risk_schema: dict
