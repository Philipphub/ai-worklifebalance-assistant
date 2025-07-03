from pydantic import BaseModel, Field
from typing import List, Dict


class ScheduleAnalysisRequest(BaseModel):
    """Request model for the schedule analysis endpoint."""

    tasks: List[str] = Field(
        ...,
        example=[
            "Prepare presentation for 10am meeting",
            "Team stand-up at 9am",
            "Call the doctor to make an appointment",
        ],
    )


class ScheduleAnalysisResponse(BaseModel):
    """Response model for the schedule analysis endpoint."""

    categorized_tasks: Dict[str, List[str]] = Field(
        ...,
        example={
            "Work": ["Prepare presentation for 10am meeting", "Team stand-up at 9am"],
            "Personal": ["Call the doctor to make an appointment"],
        },
    )
    analysis_report: str = Field(..., example="Your schedule seems balanced.")
    suggestions: List[str] = Field(
        ..., example=["Consider taking a short break after your morning meetings."]
    )
