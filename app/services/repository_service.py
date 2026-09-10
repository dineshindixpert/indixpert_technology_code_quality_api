
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Repository
from app.schemas.repository import RepositoryCreate


async def create_repository(
    db: AsyncSession,
    data: RepositoryCreate,
) -> Repository:
    repository = Repository(
        github_connection_id=data.github_connection_id,
        github_repo_id=data.github_repo_id,
        name=data.name,
        full_name=data.full_name,
        description=data.description,
        clone_url=data.clone_url,
        html_url=data.html_url,
        default_branch=data.default_branch,
        is_private=data.is_private,
        language=data.language,
    )

    db.add(repository)

    await db.commit()
    await db.refresh(repository)

    return repository


async def get_repositories(
    db: AsyncSession,
) -> list[Repository]:
    result = await db.execute(
        select(Repository).order_by(
            Repository.created_at.desc()
        )
    )

    return list(result.scalars().all())


async def get_repository(
    db: AsyncSession,
    repository_id: UUID,
) -> Repository | None:
    result = await db.execute(
        select(Repository).where(
            Repository.id == repository_id
        )
    )

    return result.scalar_one_or_none()

