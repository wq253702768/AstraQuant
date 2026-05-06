from pydantic import BaseModel


class EvidenceResponse(BaseModel):
    items: list[dict]

