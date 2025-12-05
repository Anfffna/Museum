# database.py
from sqlmodel import SQLModel, create_engine, Session
from models import (
    Employee, Hall, Supply, Ticket, Visitor,
    Exhibit, Movement, Restoration
)

# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:anna12345@localhost/museum_db"

# Create engine for database connection
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Creates all tables in the database"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Returns session for working with database"""
    with Session(engine) as session:
        yield session

# For FastAPI dependencies
def get_db():
    with Session(engine) as session:
        yield session