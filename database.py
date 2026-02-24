from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()

class ReferenceModel(Base):
    __tablename__ = 'reference_models'
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(100), nullable=False)
    model_name = Column(String(200), nullable=False)
    base_price = Column(Float, nullable=False)
    category = Column(String(50), default='camera')
    search_keywords = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProcessedAd(Base):
    __tablename__ = 'processed_ads'
    
    id = Column(Integer, primary_key=True)
    olx_ad_id = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50))
    title = Column(String(500))
    price = Column(Float)
    url = Column(String(500))
    matched_model_id = Column(Integer)
    discount_percent = Column(Float)
    first_seen = Column(DateTime, default=datetime.utcnow)
    notification_sent = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime)

class ScraperLog(Base):
    __tablename__ = 'scraper_logs'
    
    id = Column(Integer, primary_key=True)
    category = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    ads_found = Column(Integer, default=0)
    new_ads = Column(Integer, default=0)
    good_deals = Column(Integer, default=0)
    errors = Column(Text)
    status = Column(String(20))

engine = create_engine(config.DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized successfully")
