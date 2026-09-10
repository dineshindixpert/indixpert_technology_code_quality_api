
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RepositoryCreate(BaseModel):
    github_connection_id: UUID | None = None
    github_repo_id: int
    name: str
    full_name: str
    description: str | None = None
    clone_url: str
    html_url: str | None = None
    default_branch: str = "main"
    is_private: bool = False
    language: str | None = None


class RepositoryResponse(BaseModel):
    id: UUID
    github_connection_id: UUID | None

    github_repo_id: int
    name: str
    full_name: str
    description: str | None

    clone_url: str
    html_url: str | None

    default_branch: str
    is_private: bool
    language: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

