
from uuid import UUID

from pydantic import BaseModel


class GithubConnectionCreate(BaseModel):
    user_id: UUID
    github_user_id: int
    github_username: str | None = None
    access_token: str


class GithubConnectionResponse(BaseModel):
    id: UUID
    user_id: UUID
    github_user_id: int
    github_username: str | None = None

    model_config = {
        "from_attributes": True,
    }


class GithubRepositoryResponse(BaseModel):
    github_repo_id: int
    name: str
    full_name: str
    description: str | None = None
    clone_url: str
    html_url: str | None = None
    default_branch: str
    is_private: bool
    language: str | None = None

