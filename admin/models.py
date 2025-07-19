from app import db
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from datetime import datetime




class SiteSettingsModel(db.Model):
    __tablename__ = 'site_settings'
    
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=True, default='mySite')
    description = Column(String(300), nullable=True)
    logo = Column(String(100), default='assets/images/logo.png')
    email = Column(String(100), nullable=True)
    mobile = Column(String(11), nullable=True)
    phone = Column(String(11), nullable=True)
    address = Column(String(500), nullable=True)
    post_code = Column(String(10), nullable=True)
    start_time = Column(DateTime())
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    
    def __str__(self):
        return self.title


    
    
    