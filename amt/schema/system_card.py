from pydantic import (
    BaseModel,
    Field,  # pyright: ignore [reportUnknownMemberType]
)

from amt.schema.assessment_card import AssessmentCard
from amt.schema.instrument import InstrumentBase


class SystemCard(BaseModel):
    schema_version: str = Field(default="0.1a6")
    name: str = Field(default=None)
    selected_instruments: list[InstrumentBase] = Field(default=[])
    assessments: list[AssessmentCard] = Field(default=[])
