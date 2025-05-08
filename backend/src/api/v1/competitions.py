from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status

from src.models.competition import CompetitionDTO, CompetitionPreview, NewCompetition
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
        competition: NewCompetition,
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
    competition = await service.get_competition(competition_id)
    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competition not found",
        )
    return competition


@router_competitions.get(
    path="/previews",
    description="Get all competitions previews for creator",
    tags=["competitions"],
    status_code=status.HTTP_200_OK,
    name="Get all competitions previews",
)
async def get_all_competitions_previews_for_user(
        user_id: str = Query(..., description="Creator ID"),
        service: CompetitionService = Depends(get_competition_service),
) -> List[CompetitionPreview]:
    return await service.get_all_competitions_previews_for_user(user_id)


@router_competitions.get(
    path="/all",
    description="Get all competitions previews",
    tags=["competitions"],
    status_code=status.HTTP_200_OK,
    name="Get all competitions previews",
)
async def get_all_competitions_previews(
        service: CompetitionService = Depends(get_competition_service),
) -> List[CompetitionPreview]:
    return await service.get_all_competitions_previews()
