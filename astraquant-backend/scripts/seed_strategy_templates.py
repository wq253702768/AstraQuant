from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
sys.path.insert(0, str(ROOT / "services/strategy-service"))

from app.domain.services.strategy_template_service import template_seed_rows
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.strategy_template_repository import StrategyTemplateRepository

async def main() -> None:
    async with SessionLocal() as session:
        repo = StrategyTemplateRepository(session)
        for row in template_seed_rows():
            await repo.upsert_seed(row)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
