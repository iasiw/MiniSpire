from sqlalchemy import create_engine, Column, String, JSON, Integer
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

class Population(Base):
    __tablename__ = "populations"
    id = Column(Integer, primary_key=True)
    gene = Column(JSON, nullable=False)
    score = Column(Integer, default=0)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
