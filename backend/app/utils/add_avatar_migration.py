import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def ensure_avatar_column(db_path: str | Path) -> None:
    """
    Ensure the 'avatar' column exists in the 'users' table for the given SQLite DB.
    If users table does not exist, do nothing (create_all will handle it).
    This function is idempotent.
    """
    db_path = str(db_path)
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Check if users table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        row = cur.fetchone()
        if not row:
            logger.info("users table does not exist yet, skipping avatar column migration.")
            conn.close()
            return

        # Get table info and check if 'avatar' column present
        cur.execute("PRAGMA table_info(users);")
        cols = [r[1] for r in cur.fetchall()]  # second field is name
        if "avatar" in cols:
            logger.info("avatar column already exists on users table.")
            conn.close()
            return

        # Add avatar column (TEXT, nullable)
        cur.execute("ALTER TABLE users ADD COLUMN avatar TEXT;")
        conn.commit()
        logger.info("Added avatar column to users table.")
    except Exception as e:
        logger.exception("Failed to ensure avatar column: %s", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass