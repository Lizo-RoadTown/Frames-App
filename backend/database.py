"""
Database instance for FRAMES
Separate file to avoid circular imports
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
