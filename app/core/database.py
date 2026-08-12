from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings
from app.models.base import Base

# Import models so SQLAlchemy can register tables before create_all()
from app.models import transaction  # noqa: F401
from app.models import user  # noqa: F401
from app.models import wallet  # noqa: F401

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
