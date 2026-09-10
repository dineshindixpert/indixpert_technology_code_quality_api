from fastapi import FastAPI

from app.github.auth import create_github_jwt , get_app_installations ,  create_installation_token, get_installation_repositories, get_repository_contents, get_file_content

from app.github.scanner import scan_repository

app = FastAPI(
    title="Code Quality Tool",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Code Quality Tool API is running"
    }


@app.get("/github/auth-test")
def github_auth_test():
    token = create_github_jwt()

    return {
        "success": True,
        "message": "GitHub App JWT generated successfully",
        "token_preview": token[:20] + "..."
    }


@app.get("/github/installations")
async def github_installations():
    installations = await get_app_installations()

    return {
        "success": True,
        "installations": installations,
    }


@app.get("/github/token-test")
async def github_token_test():
    installation_id = 160331728

    token_data = await create_installation_token(
        installation_id
    )

    return {
        "success": True,
        "expires_at": token_data.get("expires_at"),
        "permissions": token_data.get("permissions"),
        "repository_selection": token_data.get(
            "repository_selection"
        ),
    }


@app.get("/github/repositories")
async def github_repositories():
    installation_id = 160331728

    data = await get_installation_repositories(
        installation_id
    )

    return {
        "success": True,
        "total_count": data["total_count"],
        "repositories": [
            {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "private": repo["private"],
                "default_branch": repo["default_branch"],
            }
            for repo in data["repositories"]
        ],
    }


@app.get("/github/repository/{owner}/{repo}/contents")
async def github_repository_contents(
    owner: str,
    repo: str,
    path: str = ""
):
    installation_id = 160331728

    contents = await get_repository_contents(
        installation_id=installation_id,
        owner=owner,
        repo=repo,
        path=path,
    )

    return {
        "success": True,
        "owner": owner,
        "repository": repo,
        "path": path,
        "contents": contents,
    }

@app.get("/github/repository/{owner}/{repo}/file")
async def github_file_content(
    owner: str,
    repo: str,
    path: str,
    ref: str = "main",
):
    installation_id = 160331728

    file_data = await get_file_content(
        installation_id=installation_id,
        owner=owner,
        repo=repo,
        path=path,
        ref=ref,
    )

    return {
        "success": True,
        **file_data,
    }



@app.get("/github/repository/{owner}/{repo}/scan")
async def github_scan_repository(
    owner: str,
    repo: str,
):
    installation_id = 160331728

    files = await scan_repository(
        installation_id=installation_id,
        owner=owner,
        repo=repo,
    )

    return {
        "success": True,
        "owner": owner,
        "repository": repo,
        "total_files": len(files),
        "files": files,
    }