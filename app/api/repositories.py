
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository_service import (
    create_repository,
    get_repositories,
    get_repository,
)

router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_repo(
    data: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_repository(
        db=db,
        data=data,
    )


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
async def list_repositories(
    db: AsyncSession = Depends(get_db),
):
    return await get_repositories(db=db)


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
async def get_repo(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    repository = await get_repository(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return repository

