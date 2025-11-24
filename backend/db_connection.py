from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Load environment variables from a .env file if present
load_dotenv()

_DATABASE_URL = os.getenv("DATABASE_URL")

if not _DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please add it to your .env file.")

_engine: Optional[Engine] = None

def get_engine() -> Engine:
    """Return a singleton SQLAlchemy engine configured from DATABASE_URL."""
    global _engine
    if _engine is None:
        _engine = create_engine(_DATABASE_URL)
    return _engine
