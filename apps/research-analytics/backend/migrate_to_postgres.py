"""
PostgreSQL Migration Script for FRAMES
Migrates data from SQLite to PostgreSQL

Usage:
    python migrate_to_postgres.py

Prerequisites:
    1. Install requirements: pip install -r requirements.txt
    2. Set up PostgreSQL database (local or Railway/Heroku)
    3. Update .env file with PostgreSQL connection string
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import json

# Load environment variables from parent directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)
from backend.db_connection import get_engine

# Import models
from db_models import (
    TeamModel, FacultyModel, ProjectModel, InterfaceModel,
    StudentModel, RiskFactor, FactorValue, FactorModel
)
from database import db


class PostgreSQLMigration:
    def __init__(self, sqlite_path=None, postgres_url=None):
        """
        Initialize migration with source (SQLite) and destination (PostgreSQL) databases

        Args:
            sqlite_path: Path to SQLite database (default: instance/frames.db)
            postgres_url: PostgreSQL connection string (default: from DATABASE_URL env var)
        """
        # SQLite source
        if sqlite_path is None:
            sqlite_path = os.path.join(os.path.dirname(__file__), 'instance', 'frames.db')

        if not os.path.exists(sqlite_path):
            print(f"❌ SQLite database not found at: {sqlite_path}")
            print("Creating empty SQLite database for testing...")
            self.sqlite_url = f"sqlite:///{sqlite_path}"
        else:
            self.sqlite_url = f"sqlite:///{sqlite_path}"
            print(f"✅ Found SQLite database: {sqlite_path}")

        # PostgreSQL destination
        if postgres_url is None:
            postgres_url = os.getenv('DATABASE_URL')

        if not postgres_url or postgres_url.startswith('sqlite'):
            print("❌ PostgreSQL URL not found or still using SQLite!")
            print("Please update your .env file with PostgreSQL connection string:")
            print("DATABASE_URL=postgresql://username:password@host:port/database")
            sys.exit(1)

        # Fix Heroku/Railway postgres:// -> postgresql://
        if postgres_url.startswith('postgres://'):
            postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)

        self.postgres_url = postgres_url
        print(f"✅ PostgreSQL URL configured: {postgres_url.split('@')[0]}@***")

        # Create engines
        self.sqlite_engine = create_engine(self.sqlite_url)
        self.postgres_engine = get_engine()

        # Create sessions
        SqliteSession = sessionmaker(bind=self.sqlite_engine)
        PostgresSession = sessionmaker(bind=self.postgres_engine)

        self.sqlite_session = SqliteSession()
        self.postgres_session = PostgresSession()

    def test_connections(self):
        """Test both database connections"""
        print("\n🔍 Testing database connections...")

        try:
            # Test SQLite
            inspector = inspect(self.sqlite_engine)
            sqlite_tables = inspector.get_table_names()
            print(f"✅ SQLite connected. Tables: {len(sqlite_tables)}")
            if sqlite_tables:
                print(f"   Tables: {', '.join(sqlite_tables)}")
        except Exception as e:
            print(f"❌ SQLite connection failed: {e}")
            return False

        try:
            # Test PostgreSQL
            inspector = inspect(self.postgres_engine)
            postgres_tables = inspector.get_table_names()
            print(f"✅ PostgreSQL connected. Tables: {len(postgres_tables)}")
            if postgres_tables:
                print(f"   Tables: {', '.join(postgres_tables)}")
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            print("Make sure your PostgreSQL database is running and accessible.")
            return False

        return True

    def create_postgres_schema(self):
        """Create tables in PostgreSQL database"""
        print("\n📋 Creating PostgreSQL schema...")

        try:
            # Import all models
            from database import db as flask_db
            from flask import Flask

            # Create minimal Flask app
            app = Flask(__name__)
            app.config['SQLALCHEMY_DATABASE_URI'] = self.postgres_url
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            flask_db.init_app(app)

            with app.app_context():
                # Create all tables
                flask_db.create_all()
                print("✅ PostgreSQL schema created successfully")

            return True
        except Exception as e:
            print(f"❌ Failed to create schema: {e}")
            import traceback
            traceback.print_exc()
            return False

    def migrate_table(self, model_class, table_name):
        """Migrate data from one table"""
        print(f"\n📦 Migrating {table_name}...")

        try:
            # Check if table exists in SQLite
            inspector = inspect(self.sqlite_engine)
            if table_name not in inspector.get_table_names():
                print(f"⚠️  Table '{table_name}' not found in SQLite, skipping...")
                return 0

            # Get all records from SQLite
            sqlite_records = self.sqlite_session.query(model_class).all()
            count = len(sqlite_records)

            if count == 0:
                print(f"ℹ️  No records in {table_name}")
                return 0

            # Insert into PostgreSQL
            for record in sqlite_records:
                # Convert to dict
                record_dict = record.to_dict() if hasattr(record, 'to_dict') else {
                    c.name: getattr(record, c.name) for c in record.__table__.columns
                }

                # Create new record in PostgreSQL
                postgres_record = model_class(**record_dict)
                self.postgres_session.merge(postgres_record)  # Use merge to handle duplicates

            self.postgres_session.commit()
            print(f"✅ Migrated {count} records from {table_name}")
            return count

        except Exception as e:
            print(f"❌ Failed to migrate {table_name}: {e}")
            self.postgres_session.rollback()
            import traceback
            traceback.print_exc()
            return 0

    def migrate_all(self):
        """Migrate all tables"""
        print("\n" + "="*50)
        print("🚀 Starting FRAMES PostgreSQL Migration")
        print("="*50)

        if not self.test_connections():
            return False

        if not self.create_postgres_schema():
            return False

        # Migrate all tables
        total_records = 0
        tables = [
            (ProjectModel, 'projects'),
            (TeamModel, 'teams'),
            (FacultyModel, 'faculty'),
            (InterfaceModel, 'interfaces'),
        ]

        # Try to migrate additional tables if they exist
        try:
            tables.extend([
                (StudentModel, 'students'),
                (RiskFactor, 'risk_factors'),
                (FactorValue, 'factor_values'),
                (FactorModel, 'factor_models'),
            ])
        except ImportError:
            print("ℹ️  Some models not found, migrating core tables only")

        for model, table_name in tables:
            try:
                count = self.migrate_table(model, table_name)
                total_records += count
            except Exception as e:
                print(f"⚠️  Skipping {table_name}: {e}")

        print("\n" + "="*50)
        print(f"✅ Migration Complete! Migrated {total_records} total records")
        print("="*50)

        print("\n📝 Next Steps:")
        print("1. Update your .env file to use PostgreSQL permanently")
        print("2. Test your application: python backend/app.py")
        print("3. Verify all data migrated correctly")
        print("4. Consider backing up your SQLite database")

        return True

    def close(self):
        """Close database connections"""
        self.sqlite_session.close()
        self.postgres_session.close()


def main():
    """Main migration function"""
    print("🔄 FRAMES PostgreSQL Migration Tool\n")

    # Check for PostgreSQL URL
    postgres_url = os.getenv('DATABASE_URL')
    if not postgres_url:
        print("❌ DATABASE_URL not set!")
        print("\nPlease set DATABASE_URL in your .env file:")
        print("DATABASE_URL=postgresql://username:password@host:port/database\n")
        print("Options:")
        print("1. Local PostgreSQL:")
        print("   DATABASE_URL=postgresql://postgres:password@localhost:5432/frames")
        print("\n2. Railway (sign up at railway.app):")
        print("   - Create new project")
        print("   - Add PostgreSQL database")
        print("   - Copy DATABASE_URL from variables")
        print("\n3. Heroku (sign up at heroku.com):")
        print("   - heroku addons:create heroku-postgresql:mini")
        print("   - DATABASE_URL will be set automatically")
        sys.exit(1)

    if postgres_url.startswith('sqlite'):
        print("❌ DATABASE_URL is still pointing to SQLite!")
        print("Please update to PostgreSQL connection string\n")
        sys.exit(1)

    # Run migration
    migration = PostgreSQLMigration()

    try:
        success = migration.migrate_all()
        migration.close()

        if success:
            print("\n✨ Migration successful! Your database is ready.")
            sys.exit(0)
        else:
            print("\n❌ Migration failed. Check errors above.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        migration.close()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        migration.close()
        sys.exit(1)


if __name__ == '__main__':
    main()
