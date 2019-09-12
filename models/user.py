#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place",
                              backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review",
                               backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __setattr__(self, name, value):
        """Hashes password value"""
        import hashlib
        if name == "password":
            _pass = hashlib.md5(value.encode())
            value = _pass.hexdigest()
        super.__setattr__(self, name, value)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
