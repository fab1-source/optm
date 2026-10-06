from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Company(BaseModel):
    name: str
    description: str
    audience: str = "General public"
    tone: str = "Professional and friendly"
    topics: list[str] = Field(default_factory=lambda: ["company news"])
    hashtags: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)


class PlatformConfig(BaseModel):
    enabled: bool = True
    cron: str
    page_id: str = ""


class Config(BaseModel):
    company: Company
    model: str = "claude-sonnet-5-5"
    timezone: str = "UTC"
    database: str = "optm.db"
    dry_run: bool = True
    platforms: dict[str, PlatformConfig]


def load_config(path: str | Path) -> Config:
    with open(path) as f:
        return Config.model_validate(yaml.safe_load(f))
