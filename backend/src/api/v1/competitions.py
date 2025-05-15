from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status

from src.api.v1.users import get_current_user
from src.models.competition import CompetitionDTO, CompetitionPreview, NewCompetition, CompetitionDetailedDTO
from src.service import CompetitionService, get_competition_service, get_user_service, UserService

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
        current_user: dict = Depends(get_current_user),
) -> int:
    if competition.creator_id != current_user['sub']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't create new competition not with your author id",
        )
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
) -> CompetitionDetailedDTO:
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
        user_service: UserService = Depends(get_user_service)
) -> List[CompetitionPreview]:
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
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
