# backend/run_server.py
# Programmatic launcher for the FastAPI app. Intended to be the PyInstaller entrypoint.
import os
import sys
import logging

# Ensure parent path is on sys.path so `from app.main import app` works when run from generated exe
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.main import app  # noqa: E402


def main():
    import uvicorn

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    # Disable uvicorn access log noise by default; user can override via env LOG_LEVEL
    log_level = os.environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Server terminated with an exception")
        raise