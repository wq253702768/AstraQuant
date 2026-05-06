import hashlib
import json


def calc_params_hash(params_json: dict, risk_params_json: dict) -> str:
    normalized = json.dumps(
        {"params": params_json, "risk": risk_params_json},
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
