from pydantic import BaseModel, Field
from typing import List, Dict, Optional


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
    """Enhanced response model for the schedule analysis endpoint with stress analysis and conditional rebalancing."""

    categorized_tasks: Dict[str, List[str]] = Field(
        ...,
        example={
            "Work": ["Prepare presentation for 10am meeting", "Team stand-up at 9am"],
            "Personal": ["Call the doctor to make an appointment"],
        },
    )
    analysis_report: str = Field(..., example="Your schedule seems balanced.")
    stress_level: int = Field(..., example=5, description="Stress level from 1-10")
    workload_assessment: str = Field(..., example="moderate", description="Workload assessment")
    key_concerns: List[str] = Field(
        ..., 
        example=["Back-to-back meetings without breaks"], 
        description="Main concerns identified"
    )
    needs_rebalancing: bool = Field(..., example=False, description="Whether schedule needs rebalancing")
    
    # Standard suggestions (present when stress level is manageable)
    suggestions: Optional[List[str]] = Field(
        None, 
        example=["Consider taking a short break after your morning meetings."],
        description="Standard suggestions for manageable schedules"
    )
    
    # Priority rebalancing fields (present when stress level is high)
    rebalance_report: Optional[str] = Field(
        None, 
        example="Your schedule is overwhelming and needs immediate adjustment.",
        description="Detailed rebalancing report for high-stress scenarios"
    )
    urgent_actions: Optional[List[str]] = Field(
        None, 
        example=["Cancel non-essential meetings immediately"],
        description="Immediate actions to reduce stress"
    )
    tasks_to_reschedule: Optional[List[str]] = Field(
        None, 
        example=["Prepare presentation for 10am meeting"],
        description="Tasks that should be moved to another day"
    )
    tasks_to_delegate: Optional[List[str]] = Field(
        None, 
        example=["Team stand-up at 9am"],
        description="Tasks that could be delegated"
    )
    recovery_suggestions: Optional[List[str]] = Field(
        None, 
        example=["Take a 15-minute walk to clear your mind"],
        description="Stress recovery recommendations"
    )
