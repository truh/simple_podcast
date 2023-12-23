import uvicorn

from .settings import LISTEN_HOST, LISTEN_PORT


def main():
    uvicorn.run(
        "simplepodcast.simplepodcast:app",
        host=LISTEN_HOST,
        port=LISTEN_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
