from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Define the database URL. 
# We are using SQLite, which saves the entire database into a local file named 'trust_gap.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./trust_gap.db"

# 2. Create the Database Engine.
# The engine is the core interface to the database. 
# The 'check_same_thread' argument is a specific requirement for SQLite to allow 
# multiple web requests to access the database at the same time.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a Session Factory.
# Whenever a user visits our website, we need a temporary "Session" to talk to the database.
# SessionLocal is a factory that will generate these temporary connections for us.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class.
# We will inherit from this 'Base' class when we define our tables in models.py.
# It registers all our tables so SQLAlchemy knows how to create them in SQLite.
Base = declarative_base()