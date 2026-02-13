from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime

from app.db.base import Base

# User sınıfı
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    createtime = Column(DateTime, default=datetime.datetime.now)
    role = Column(String, default="user")

    def __init__(self, username, password, email, role="user"):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.is_active = True
        self.createtime = datetime.datetime.now()
