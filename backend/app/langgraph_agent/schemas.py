from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class CategorizedTasks(BaseModel):
    """
    A Pydantic model to structure the output of the task categorization node.
    This ensures the LLM returns a clean, predictable dictionary.
    """

    categorized_tasks: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description=(
            "A dictionary where keys are categories (e.g., 'Work', 'Personal', 'Health') "
            "and values are the lists of tasks belonging to that category."
        ),
    )


class EnhancedAnalysisResult(BaseModel):
    """
    Enhanced analysis result that includes stress level and workload assessment.
    This enables conditional routing based on analysis outcomes.
    """

    analysis_report: Optional[str] = Field(
        default=None,
        description="A high-level analysis of the day's schedule, identifying potential balance issues or stress points.",
    )
    stress_level: Optional[int] = Field(
        default=None,
        description="Stress level from 1-10 (1=very relaxed, 10=extremely overwhelming)",
    )
    workload_assessment: Optional[str] = Field(
        default=None,
        description="Assessment of workload: 'light', 'moderate', 'heavy', or 'overwhelming'",
    )
    key_concerns: Optional[List[str]] = Field(
        default=None,
        description="List of main concerns or issues identified in the schedule",
    )
    needs_rebalancing: Optional[bool] = Field(
        default=None,
        description="Whether the schedule needs immediate rebalancing due to stress or overload",
    )


class AnalysisResult(BaseModel):
    """
    A Pydantic model to structure the final analysis and suggestions.
    This ensures the LLM provides both a report and actionable advice.
    """

    analysis_report: Optional[str] = Field(
        default=None,
        description="A high-level analysis of the day's schedule, identifying potential balance issues or stress points.",
    )
    suggestions: Optional[List[str]] = Field(
        default=None,
        description="A list of 2-3 clear, helpful, and non-judgmental suggestions to help the user optimize their day.",
    )


class PriorityRebalanceResult(BaseModel):
    """
    Result from priority rebalancing node for high-stress scenarios.
    Provides more aggressive recommendations for schedule optimization.
    """

    rebalance_report: Optional[str] = Field(
        default=None,
        description="Analysis of why rebalancing is needed and what changes are recommended",
    )
    urgent_actions: Optional[List[str]] = Field(
        default=None,
        description="List of immediate actions to reduce stress and workload",
    )
    tasks_to_reschedule: Optional[List[str]] = Field(
        default=None,
        description="Tasks that should be moved to another day or time",
    )
    tasks_to_delegate: Optional[List[str]] = Field(
        default=None,
        description="Tasks that could be delegated to others",
    )
    recovery_suggestions: Optional[List[str]] = Field(
        default=None,
        description="Suggestions for stress recovery and self-care",
    )
