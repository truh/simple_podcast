import os
import shutil
from pathlib import Path
from typing import List

import aiofiles
from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from settings import UPLOAD_DIR, BASE_URL


def get_all_podcasts(
    db: Session, offset: int = 0, limit: int = 100
) -> List[models.Podcast]:
    return db.query(models.Podcast).offset(offset).limit(limit).all()


def get_podcast(db: Session, podcast_id: int) -> models.Podcast:
    return db.query(models.Podcast).filter(models.Podcast.id == podcast_id).first()


def create_podcast(db: Session, podcast: schemas.PodcastBase) -> models.Podcast:
    db_podcast = models.Podcast(
        name=podcast.name, description=podcast.description, explicit=podcast.explicit
    )
    db.add(db_podcast)
    db.commit()
    db.refresh(db_podcast)
    return db_podcast


def create_episode(
    db: Session, podcast_id: int, episode: schemas.EpisodeCreate
) -> models.Episode:
    db_episode = models.Episode(
        summary=episode.summary,
        long_summary=episode.long_summary,
        title=episode.title,
        subtitle=episode.subtitle,
        url="",
        size=0,
        duration=episode.duration,
        podcast_id=podcast_id,
    )
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)

    upload_dir = Path(UPLOAD_DIR) / f"podcast_{podcast_id}" / f"episode_{db_episode.id}"
    upload_path = upload_dir / episode.filename
    if not upload_dir == upload_path.parent:
        raise HTTPException(status_code=404, detail="Invalid filename")

    try:
        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(episode.upload_file.file, buffer)
    finally:
        episode.upload_file.file.close()

    db_episode.url = f"{BASE_URL}/download/podcast_{podcast_id}/episode_{db_episode.id}/{episode.filename}"
    db_episode.size = os.path.getsize(str(upload_path))
    db.commit()
    db.refresh(db_episode)

    return db_episode
