import datetime
from pathlib import Path
from typing import Dict

import podgen

from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

import models
import schemas
import utils
from database import SessionLocal, engine
from schemas import Podcast, PodcastBase, EpisodeCreate, Episode
from settings import UPLOAD_DIR, BASE_URL

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.get("/podcast")
def list_podcasts(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Dict[str, str]:
    db_podcasts = utils.get_all_podcasts(db, offset, limit)
    return {podcast.name: f"{BASE_URL}/podcast/{podcast.id}" for podcast in db_podcasts}


@app.get("/podcast/{podcast_id}", response_model=schemas.Podcast)
def read_podcast(podcast_id: int, db: Session = Depends(get_db)) -> Podcast:
    db_podcast = utils.get_podcast(db, podcast_id)
    if db_podcast is None:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return db_podcast


@app.post("/podcast", response_model=schemas.Podcast)
def create_podcast(podcast: PodcastBase, db: Session = Depends(get_db)) -> Podcast:
    return utils.create_podcast(db, podcast)


@app.post("/podcast/{podcast_id}/episode", response_model=schemas.Episode)
def create_episode(podcast_id: int, upload_file: UploadFile = File(...), summary: str = Form(...), long_summary: str = Form(...), title: str = Form(...), subtitle: str = Form(...), duration: datetime.timedelta = Form(...), db: Session = Depends(get_db)) -> Episode:
    db_podcast = utils.get_podcast(db, podcast_id)
    if db_podcast is None:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return utils.create_episode(db, podcast_id, summary, long_summary, title, subtitle, duration, upload_file)


app.mount("/download", StaticFiles(directory=str(UPLOAD_DIR)), name="download")


@app.get("/podcast/{podcast_id}/feed.rss")
def read_podcast_feed(podcast_id: int, db: Session = Depends(get_db)):
    db_podcast = utils.get_podcast(db, podcast_id)
    if db_podcast is None:
        raise HTTPException(status_code=404, detail="Podcast not found")

    p = podgen.Podcast(
        name=db_podcast.name,
        website=BASE_URL,
        description=db_podcast.description,
        explicit=db_podcast.explicit,
    )
    p.episodes += [
        podgen.Episode(
            summary=podgen.htmlencode(db_episode.summary),
            long_summary=podgen.htmlencode(db_episode.long_summary),
            title=db_episode.title,
            subtitle=db_episode.subtitle,
            media=podgen.Media(
                url=db_episode.url,
                size=db_episode.size,
                duration=datetime.timedelta(db_episode.duration),
            ),
        )
        for db_episode in db_podcast.episodes
    ]
    return Response(p.rss_str(), headers={"Content-Type": "application/rss+xml"})
