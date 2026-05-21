import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def ensure_avatar_column(db_path: str | Path) -> None:
    """
    Ensure the 'avatar' and 'liked' columns exist in the 'users' table for the given SQLite DB.
    If users table does not exist, do nothing (create_all will handle it).
    This function is idempotent.
    """
    db_path = str(db_path)
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Check if users table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        row = cur.fetchone()
        if not row:
            logger.info("users table does not exist yet, skipping avatar/liked column migration.")
            return

        # Get table info and check if 'avatar' and 'liked' columns present
        cur.execute("PRAGMA table_info(users);")
        cols = [r[1] for r in cur.fetchall()]  # second field is name

        if "avatar" not in cols:
            try:
                cur.execute("ALTER TABLE users ADD COLUMN avatar TEXT;")
                conn.commit()
                logger.info("Added avatar column to users table.")
            except Exception:
                logger.exception("Failed to add avatar column to users table.")

        if "liked" not in cols:
            try:
                # liked stored as TEXT (JSON string or comma-separated list)
                cur.execute("ALTER TABLE users ADD COLUMN liked TEXT DEFAULT '';")
                conn.commit()
                logger.info("Added liked column to users table.")
            except Exception:
                logger.exception("Failed to add liked column to users table.")

    except Exception as e:
        logger.exception("Failed to ensure avatar/liked columns: %s", e)
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass