from datetime import timedelta
from typing import List

from pydantic import BaseModel


class EpisodeBase(BaseModel):
    summary: str
    long_summary: str = ""
    title: str
    subtitle: str = ""
    url: str
    size: int
    duration: timedelta
    file: str = ""


class Episode(EpisodeBase):
    id: int
    podcast_id: int

    class Config:
        orm_mode = True


class PodcastBase(BaseModel):
    name: str
    description: str
    explicit: bool
    episodes: List[EpisodeBase] = []


class Podcast(BaseModel):
    id: int

    class Config:
        orm_mode = True
