from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.settings import UserSettings
from app.schemas.settings import UserSettingsResponse, UserSettingsUpdate, AnalysisSettings

router = APIRouter()

_DEFAULTS = AnalysisSettings()


@router.get("/settings", response_model=UserSettingsResponse)
async def get_settings(db: AsyncSession = Depends(get_db)):
    row = (
        await db.execute(select(UserSettings).where(UserSettings.id == 1))
    ).scalar_one_or_none()
    if not row:
        return UserSettingsResponse()
    return UserSettingsResponse(analysis=AnalysisSettings(**row.analysis))


@router.put("/settings", response_model=UserSettingsResponse)
async def update_settings(body: UserSettingsUpdate, db: AsyncSession = Depends(get_db)):
    if body.analysis is None:
        return await get_settings(db)

    row = (
        await db.execute(select(UserSettings).where(UserSettings.id == 1))
    ).scalar_one_or_none()

    if not row:
        row = UserSettings(id=1, analysis=body.analysis.model_dump())
        db.add(row)
    else:
        row.analysis = body.analysis.model_dump()

    await db.flush()
    return UserSettingsResponse(analysis=body.analysis)
