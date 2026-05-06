from jsonschema import Draft202012Validator
from astra_common.errors import AppError

AGENT_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["agent_name", "conclusion", "evidence", "risk_level", "suggestions", "confidence"],
    "properties": {
        "agent_name": {"type": "string"},
        "conclusion": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "risk_level": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]},
        "suggestions": {"type": "array"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "additionalProperties": True,
}

class AIOutputValidator:
    def validate(self, output: dict) -> None:
        errors = sorted(Draft202012Validator(AGENT_OUTPUT_SCHEMA).iter_errors(output), key=lambda e: list(e.path))
        if errors:
            first = errors[0]
            path = ".".join(str(item) for item in first.path) or "root"
            raise AppError("AI_OUTPUT_SCHEMA_INVALID", f"{path}: {first.message}", 422)
        for suggestion in output.get("suggestions", []):
            if suggestion.get("type") in {"PARAMETER_CHANGE", "PARAMETER_SET", "RISK_CHANGE"} and suggestion.get("need_retest") is not True:
                raise AppError("AI_OUTPUT_SCHEMA_INVALID", "参数/风控建议必须 need_retest=true", 422)
