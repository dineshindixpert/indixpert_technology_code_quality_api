
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.github import (
    GithubConnectionCreate,
    GithubConnectionResponse,
    GithubRepositoryResponse,
)
from app.services.github_service import (
    create_github_connection,
    get_github_connection,
    get_github_repositories,
)


router = APIRouter(
    prefix="/api/github",
    tags=["GitHub"],
)


@router.post(
    "/connect",
    response_model=GithubConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def connect_github(
    data: GithubConnectionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_github_connection(
        db=db,
        data=data,
    )


@router.get(
    "/status/{user_id}",
    response_model=GithubConnectionResponse,
)
async def github_status(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    connection = await get_github_connection(
        db=db,
        user_id=user_id,
    )

    if connection is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="GitHub connection not found",
        )

    return connection


@router.get(
    "/repositories/{user_id}",
    response_model=list[GithubRepositoryResponse],
)
async def github_repositories(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await get_github_repositories(
        db=db,
        user_id=user_id,
    )

