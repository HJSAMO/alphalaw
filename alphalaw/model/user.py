# -*- coding: utf-8 -*-
"""
    alphalaw.model.user
    ~~~~~~~~~~~~~~~~~~~
    alphalaw 어플리케이션을 사용할 사용자 정보에 대한 model 모듈.
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from alphalaw.model import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=False)
    password = Column(String(55), unique=False)

    contracts = relationship('Contract', 
                          backref='user', 
                          cascade='all, delete, delete-orphan')
    
    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)