from src.configs.env import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextvars import ContextVar

config = get_settings()

engine = create_engine(
    "postgresql://{user}:{password}@{host}/{db_name}".format(
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        db_name=config.db_name,
    )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

db_session: ContextVar[Session] = ContextVar("db_session", default=None)

def get_db() -> Session:
    """Get DB session stored in context var or create a new one."""
    session = db_session.get()
    if session is None:
        session = SessionLocal()
        db_session.set(session)
    return session

def clear_db_session():
    """Clear and close DB session"""
    session = db_session.get()
    if session:
        session.close()
        db_session.set(None)

def select_all(rows):
    """Select all rows"""
    db = get_db()
    try:
        return rows.all()
    except Exception:
        db.rollback()
        clear_db_session()
        db = get_db()
        return rows.all()

def select_first(rows):
    """Select first row"""
    db = get_db()
    try:
        return rows.first()
    except Exception:
        db.rollback()
        clear_db_session()
        db = get_db()
        return rows.first()

def select_count(rows):
    """Count rows"""
    db = get_db()
    try:
        return rows.count()
    except Exception:
        db.rollback()
        clear_db_session()
        db = get_db()
        return rows.count()

def save_new_row(new_row):
    """Save new row"""
    db = get_db()
    try:
        db.add(new_row)
        db.commit()
        db.refresh(new_row)
        return new_row
    except Exception as e:
        db.rollback()
        raise e
    finally:
        clear_db_session()

def update_old_row(old_row):
    """Update existing row"""
    db = get_db()
    try:
        db.commit()
        db.refresh(old_row)
        return old_row
    except Exception as e:
        db.rollback()
        raise e
    finally:
        clear_db_session()

def delete(old_row):
    """Delete a row"""
    db = get_db()
    try:
        db.delete(old_row)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        clear_db_session()
