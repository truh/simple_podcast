from os import environ
from pathlib import Path

from starlette.config import Config

__config = Config(environ.get("SIMPLEPODCAST_CONFIG", ".env"))

UPLOAD_DIR: Path = __config.get("UPLOAD_DIR", Path, "data/uploads")
SQLALCHEMY_DATABASE_URL: str = __config.get(
    "SQLALCHEMY_DATABASE_URL", str, "sqlite:///./data/test.sqlite3"
)
PUBLIC_URL: str = __config.get("PUBLIC_URL", str, "http://localhost:8000")
LISTEN_PORT: int = __config.get("LISTEN_PORT", int, 8090)
LISTEN_HOST: str = __config.get("LISTEN_PORT", str, "127.0.0.1")
