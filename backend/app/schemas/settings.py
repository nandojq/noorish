from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class AnalysisSettings(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    deficiency_threshold_percent_dv: int = 70
    excess_threshold_percent_dv: int = 150


class UserSettingsResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    analysis: AnalysisSettings = AnalysisSettings()


class UserSettingsUpdate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    analysis: Optional[AnalysisSettings] = None

    @field_validator("analysis")
    @classmethod
    def validate_analysis(cls, v: Optional[AnalysisSettings]) -> Optional[AnalysisSettings]:
        if v is None:
            return v
        if v.deficiency_threshold_percent_dv >= 100:
            raise ValueError("deficiencyThresholdPercentDv must be < 100")
        if v.excess_threshold_percent_dv <= 100:
            raise ValueError("excessThresholdPercentDv must be > 100")
        return v
