from typing import Any

from app.github.auth import get_repository_contents


SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cs",
    ".c",
    ".cpp",
    ".h",
    ".go",
    ".rs",
}


IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".next",
    "coverage",
}


def is_source_file(filename: str) -> bool:
    filename = filename.lower()

    return any(
        filename.endswith(extension)
        for extension in SOURCE_EXTENSIONS
    )


def should_ignore(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")

    return any(
        part in IGNORED_DIRECTORIES
        for part in parts
    )


async def scan_repository(
    installation_id: int,
    owner: str,
    repo: str,
    path: str = "",
) -> list[dict[str, Any]]:

    if should_ignore(path):
        return []

    contents = await get_repository_contents(
        installation_id=installation_id,
        owner=owner,
        repo=repo,
        path=path,
    )

    if isinstance(contents, dict):
        contents = [contents]

    files = []

    for item in contents:

        item_path = item["path"]
        item_type = item["type"]
        item_name = item["name"]

        if should_ignore(item_path):
            continue

        # -------------------------
        # FILE
        # -------------------------

        if item_type == "file":

            if not is_source_file(item_name):
                continue

            files.append(
                {
                    "name": item_name,
                    "path": item_path,
                    "sha": item.get("sha"),
                    "size": item.get("size", 0),
                }
            )

        # -------------------------
        # DIRECTORY
        # -------------------------

        elif item_type == "dir":

            nested_files = await scan_repository(
                installation_id=installation_id,
                owner=owner,
                repo=repo,
                path=item_path,
            )

            files.extend(nested_files)

    return files