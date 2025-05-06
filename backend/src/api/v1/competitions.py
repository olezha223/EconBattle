from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from src.models.competition import CompetitionDTO
from src.service import CompetitionService, get_competition_service

router_competitions = APIRouter(
    prefix="/competitions",
    tags=["competitions"],
)


@router_competitions.post(
    path="/",
    description="Create a new competition",
    tags=["competitions"],
    status_code=status.HTTP_201_CREATED,
    name="Create Competition",
)
async def create_competition(
        competition: CompetitionDTO,
        service: CompetitionService = Depends(get_competition_service),
) -> int:
    return await service.create_competition(competition)

@router_competitions.get(
    path="/",
    description="Get competition by id",
    tags=["competitions"],
    status_code=status.HTTP_200_OK,
    name="Get Competition",
)
async def get_competition_by_id(
        competition_id: int = Query(..., description="ID of the competition to retrieve"),
        service: CompetitionService = Depends(get_competition_service),
) -> CompetitionDTO:
    return await service.get_competition(competition_id)
