from sqlalchemy import Boolean, Column, ForeignKey, Integer, Interval, String
from sqlalchemy.orm import relationship
from .database import Base


class Episode(Base):
    __tablename__ = "episode"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String)
    long_summary = Column(String)
    title = Column(String)
    subtitle = Column(String)

    url = Column(String)
    size = Column(Integer)
    duration = Column(Interval)
    file = Column(String)

    podcast_id = Column(Integer, ForeignKey("podcast.id"))
    podcast = relationship("Podcast", back_populates="episodes")


class Podcast(Base):
    __tablename__ = "podcast"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    explicit = Column(Boolean)

    episodes = relationship("Episode", back_populates="podcast")
