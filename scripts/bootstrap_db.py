from __future__ import annotations

import sys
from pathlib import Path

# Add backend to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend import db_models  # Ensure models are registered with metadata
from backend.db_connection import get_engine
from backend.database import db

Base = db.Model


def main() -> None:
    print("Bootstrapping database schema...")
    engine = get_engine()
    try:
        Base.metadata.create_all(bind=engine)
        print("Database schema created successfully.")
    except Exception as exc:
        print(f"Database bootstrap failed: {exc}")
        sys.exit(1)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
