from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from MiniSpire.src.config import game_config



engine = create_engine(game_config.DATABASE_URL)
Base = declarative_base()
class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(String(36), primary_key=True)
    saved_cards = Column(JSON, default=[])

class User(Base):
    __tablename__ = "users"
    username = Column(String(36),primary_key=True)
    password = Column(String(36))
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
