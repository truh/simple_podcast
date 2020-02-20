import datetime
from typing import Dict

import podgen

from fastapi import FastAPI
from starlette.responses import Response

from schemas import Podcast, PodcastBase, EpisodeBase, Episode

BASE_URL = "http://localhost:8000"


app = FastAPI()


@app.get("/podcast")
def list_podcasts() -> Dict[str, str]:
    return {"podcast": f"{BASE_URL}/podcast/1"}


@app.get("/podcast/{podcast_id}")
def read_podcast(podcast_id: int) -> Podcast:
    return Podcast()


@app.post("/podcast")
def create_podcast(podcast: PodcastBase) -> Podcast:
    return Podcast()


@app.post("/podcast/{podcast_id}/episode")
def create_episode(podcast_id: int, episode: EpisodeBase) -> Episode:
    return Episode()


@app.get("/podcast/{podcast_id}/feed.rss")
def read_podcast_feed(podcast_id: int):
    p = podgen.Podcast(
        name="Podcast Name",
        website=BASE_URL,
        description="Podcast description",
        explicit=False,
    )
    p.episodes += [
        podgen.Episode(
            summary=podgen.htmlencode("Episode 1"),
            long_summary=podgen.htmlencode("Episode 1 Long Summary"),
            title="Episode 1",
            subtitle="Subtitle",
            media=podgen.Media(
                url="http://example.com/a.mp3",
                size=12345,
                duration=datetime.timedelta(minutes=123),
            ),
        )
    ]
    return Response(p.rss_str(), headers={"Content-Type": "application/rss+xml"})
