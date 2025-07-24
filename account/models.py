from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from persiantools.jdatetime import JalaliDateTime



class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer(), primary_key=True)
    email = Column(String(128), nullable=True, unique=True)
    phone = Column(String(11), nullable=True, unique=True)
    full_name = Column(String(128), nullable=True)
    avatar = Column(String(125), default='images/users/avatar/avatar.png')
    username = Column(String(128), nullable=True, unique=True)
    password = Column(String(500), nullable=True)
    role = Column(Integer(), nullable=False, default=2)
    gender = Column(Boolean(), default=True)
    email_token = Column(String(150), nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    logs = db.relationship('UserLogModel', backref='user')

    def __repr__(self):
        return f'{self.id} :: {self.phone}'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def is_superuser(self):
        return self.role == 0
    
    def is_admin(self):
        return self.role <= 1
    
    def is_staff(self):
        return self.role == 2
    
    def sex(self):
        return 'male' if self.gender==True else 'female'
    
    def last_login(self):
        log =  UserLogModel.query.filter_by(user_id=self.id).order_by(UserLogModel.id.desc()).first()
        if log:
            return [JalaliDateTime(log.login_at).strftime('%Y-%m-%d'), JalaliDateTime(log.login_at).strftime('%H:%M')]
    
    
class UserPhoneModel(db.Model):
    __tablename__ = 'users_phone'
    
    id = Column(Integer(), primary_key=True)
    phone = Column(String(11), nullable=True)
    code = Column(String(6), nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    expired_at = Column(DateTime(), nullable=True)
    
    def __str__(self):
        return f'{self.phone} : {self.created_at} - {self.expired_at}'
    
    
    
class UserLogModel(db.Model):
    __tablename__ = 'users_log'
    
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    login_at = Column(DateTime(), nullable=True)
    logout_at = Column(DateTime(), nullable=True)
    is_active = Column(Boolean(), default=False)
    
    def __str__(self):
        return f'from {self.login_at} to {self.logout_at}'
    