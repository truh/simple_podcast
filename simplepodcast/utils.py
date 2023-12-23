import logging
import os
import shutil
from datetime import timedelta
from pathlib import Path
from typing import List
from urllib.parse import quote

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from . import models, schemas
from .settings import PUBLIC_URL, UPLOAD_DIR


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
    db: Session,
    podcast_id: int,
    title: str,
    subtitle: str,
    summary: str,
    long_summary: str,
    duration: timedelta,
    upload_file: UploadFile,
) -> models.Episode:
    db_episode = models.Episode(
        summary=summary,
        long_summary=long_summary,
        title=title,
        subtitle=subtitle,
        url="",
        size=0,
        duration=duration,
        podcast_id=podcast_id,
    )
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)

    filename = upload_file.filename

    upload_dir = Path(UPLOAD_DIR) / f"podcast_{podcast_id}" / f"episode_{db_episode.id}"
    upload_path = upload_dir / filename
    if not upload_dir == upload_path.parent:
        raise HTTPException(status_code=404, detail="Invalid filename")

    try:
        upload_dir.mkdir(parents=True, exist_ok=True)
        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except OSError as e:
        db.delete(db_episode)
        upload_file.file.close()
        logging.exception("Unable to store upload to disk. %s", e)
        raise HTTPException(500, "Unable to store upload to disk. " + str(e))
    finally:
        upload_file.file.close()

    db_episode.url = "%s/download/podcast_%d/episode_%d/%s" % (
        PUBLIC_URL,
        podcast_id,
        db_episode.id,
        quote(filename),
    )
    db_episode.size = os.path.getsize(str(upload_path))
    db.commit()
    db.refresh(db_episode)

    return db_episode
