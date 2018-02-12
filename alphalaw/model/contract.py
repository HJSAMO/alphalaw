# -*- coding: utf-8 -*-
"""
    alphalaw.model.contract
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    alphalaw 어플리케이션을 사용할 사용자 정보에 대한 model 모듈.
"""


from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime

from alphalaw.model.user import User

from alphalaw.model import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    filename_orig = Column(String(400), unique=False)
    filename = Column(String(400), unique=False)
    filesize = Column(Integer, unique=False)
    upload_date = Column(DateTime, unique=False)

    def __init__(self, user_id, filename_orig, filename, filesize, upload_date):
        """Contract 모델 클래스를 초기화 한다."""
        
        self.user_id = user_id
        self.filename_orig = filename_orig
        self.filename = filename
        self.filesize = filesize
        self.upload_date = upload_date


    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<Contract %r %r>' % (self.user_id, self.upload_date)