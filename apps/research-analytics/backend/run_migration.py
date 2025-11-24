"""
Wrapper to run migration with proper encoding for Windows
"""
import sys
import os

# Set UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env
from dotenv import load_dotenv
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

# Verify it loaded
db_url = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {db_url[:30]}..." if db_url else "DATABASE_URL not loaded!")

# Now run the actual migration
import migrate_to_postgres
migrate_to_postgres.main()
