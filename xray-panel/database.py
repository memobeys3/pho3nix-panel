from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pho3nix_panel.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    uuid = Column(String, unique=True, index=True, nullable=False)
    port = Column(Integer, nullable=False)
    quota_bytes = Column(BigInteger, default=0)
    used_bytes = Column(BigInteger, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_traffic_update = Column(DateTime, default=datetime.datetime.utcnow)

class TrafficLog(Base):
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    bytes_up = Column(BigInteger, default=0)
    bytes_down = Column(BigInteger, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
