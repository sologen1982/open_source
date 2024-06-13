from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String(100), index=True, unique=True)
    phone = Column(String(20), index=True)
    birthday = Column(Date, index=True)
    additional_info = Column(String(250), nullable=True)
    completed = Column(Boolean, default=False)
