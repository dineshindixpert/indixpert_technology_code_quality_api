
from uuid import UUID

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import GithubConnection
from app.schemas.github import (
    GithubConnectionCreate,
    GithubRepositoryResponse,
)


GITHUB_API_URL = "https://api.github.com"


async def create_github_connection(
    db: AsyncSession,
    data: GithubConnectionCreate,
):
    connection = GithubConnection(
        user_id=data.user_id,
        github_user_id=data.github_user_id,
        github_username=data.github_username,
        access_token=data.access_token,
    )

    db.add(connection)
    await db.commit()
    await db.refresh(connection)

    return connection


async def get_github_connection(
    db: AsyncSession,
    user_id: UUID,
):
    result = await db.execute(
        select(GithubConnection).where(
            GithubConnection.user_id == user_id
        )
    )

    return result.scalar_one_or_none()


async def get_github_repositories(
    db: AsyncSession,
    user_id: UUID,
):
    connection = await get_github_connection(
        db=db,
        user_id=user_id,
    )

    if connection is None:
        raise HTTPException(
            status_code=404,
            detail="GitHub connection not found",
        )

    headers = {
        "Authorization": f"Bearer {connection.access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{GITHUB_API_URL}/user/repos",
            headers=headers,
            params={
                "per_page": 100,
                "sort": "updated",
            },
        )

    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired GitHub access token",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch repositories from GitHub",
        )

    repositories = response.json()

    return [
        GithubRepositoryResponse(
            github_repo_id=repo["id"],
            name=repo["name"],
            full_name=repo["full_name"],
            description=repo.get("description"),
            clone_url=repo["clone_url"],
            html_url=repo.get("html_url"),
            default_branch=repo.get("default_branch") or "main",
            is_private=repo["private"],
            language=repo.get("language"),
        )
        for repo in repositories
    ]

