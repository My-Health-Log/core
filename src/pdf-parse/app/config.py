from pathlib import Path

import tomllib
from pydantic_settings import BaseSettings


def get_project_meta():
    with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as f:
        return tomllib.load(f)["project"]


_project = get_project_meta()


class Settings(BaseSettings):
    cors_origins: list[str] = ["http://localhost:3000"]
    title: str = _project["name"]
    description: str = _project["description"]
    version: str = _project["version"]


settings = Settings()
