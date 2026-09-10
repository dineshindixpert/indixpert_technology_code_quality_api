import os
import time
from pathlib import Path
import httpx
import jwt
from dotenv import load_dotenv
import base64

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")


def create_github_jwt():
    if not GITHUB_APP_ID:
        raise ValueError("GITHUB_APP_ID is missing")

    if not PRIVATE_KEY_PATH:
        raise ValueError("GITHUB_PRIVATE_KEY_PATH is missing")

    key_path = BASE_DIR / PRIVATE_KEY_PATH

    if not key_path.exists():
        raise FileNotFoundError(
            f"Private key not found: {key_path}"
        )

    private_key = key_path.read_text()

    now = int(time.time())

    payload = {
        "iat": now - 60,
        "exp": now + (9 * 60),
        "iss": GITHUB_APP_ID,
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )


async def get_app_installations():
    jwt_token = create_github_jwt()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/app/installations",
            headers=headers,
        )

    response.raise_for_status()

    return response.json()

async def create_installation_token(installation_id: int):
    jwt_token = create_github_jwt()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = (
        f"https://api.github.com/app/installations/"
        f"{installation_id}/access_tokens"
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
        )

    print("GitHub status:", response.status_code)
    print("GitHub response:", response.text)

    response.raise_for_status()

    return response.json()


async def get_installation_repositories(
    installation_id: int
):
    token_data = await create_installation_token(
        installation_id
    )

    installation_token = token_data["token"]

    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = "https://api.github.com/installation/repositories"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
        )

    response.raise_for_status()

    return response.json()

async def get_repository_contents(
    installation_id: int,
    owner: str,
    repo: str,
    path: str = ""
):
    token_data = await create_installation_token(
        installation_id
    )

    installation_token = token_data["token"]

    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
        )

    response.raise_for_status()

    return response.json()


async def get_file_content(
    installation_id: int,
    owner: str,
    repo: str,
    path: str,
    ref: str = "main",
):
    token_data = await create_installation_token(
        installation_id
    )

    installation_token = token_data["token"]

    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    params = {
        "ref": ref
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            params=params,
        )

    response.raise_for_status()

    file_data = response.json()

    encoded_content = file_data.get("content", "")

    decoded_content = base64.b64decode(
        encoded_content
    ).decode("utf-8")

    return {
        "name": file_data.get("name"),
        "path": file_data.get("path"),
        "sha": file_data.get("sha"),
        "size": file_data.get("size"),
        "content": decoded_content,
    }