from fastapi import APIRouter
from app.api.v1 import schemas
from app.services import analysis_service

router = APIRouter()


@router.post(
    "/analyze-schedule",
    response_model=schemas.ScheduleAnalysisResponse,
    tags=["Analysis"],
)
def analyze_schedule(request: schemas.ScheduleAnalysisRequest):
    """
    Analyzes a list of tasks and returns categorizations, a report, and suggestions.
    """
    # Call the analysis service with the user's tasks
    result = analysis_service.analyze_schedule_service(request.tasks)

    # The service returns a dictionary, which we can directly pass into our response model
    return schemas.ScheduleAnalysisResponse(**result)
