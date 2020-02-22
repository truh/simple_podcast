from datetime import timedelta
from typing import List

from pydantic import BaseModel


class EpisodeBase(BaseModel):
    summary: str
    long_summary: str = ""
    title: str
    subtitle: str = ""
    duration: timedelta


class EpisodeCreate(EpisodeBase):
    filename: str


class Episode(EpisodeBase):
    id: int
    podcast_id: int
    url: str
    size: int

    class Config:
        orm_mode = True


class PodcastBase(BaseModel):
    name: str
    description: str
    explicit: bool


class Podcast(BaseModel):
    id: int
    episodes: List[EpisodeBase] = []

    class Config:
        orm_mode = True
