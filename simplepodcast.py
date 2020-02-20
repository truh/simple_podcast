import datetime

import podgen

from fastapi import FastAPI
from starlette.responses import Response


BASE_URL = "http://localhost:8000"


app = FastAPI()


@app.get("/podcast/")
def list_podcasts():
    return {"podcast": "World"}


@app.get("/podcast/{podcast_id}/")
def read_podcast(podcast_id: str):
    return {"item_id": podcast_id}


@app.post("/podcast/")
def create_podcast(podcast_id: str):
    return {"item_id": podcast_id}


@app.post("/podcast/{podcast_id}/episode/")
def create_episode(podcast_id: str):
    return {"item_id": podcast_id}


@app.get("/podcast/{podcast_id}.rss")
def read_podcast_feed(podcast_id: str):
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
