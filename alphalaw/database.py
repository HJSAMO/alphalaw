# -*- coding: utf-8 -*-
"""
    alphalaw.database
    ~~~~~~~~~~~~~~~~~
    DB 연결 및 쿼리 사용을 위한 공통 모듈.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBManager:
    """데이터베이스 처리를 담당하는 공통 클래스"""
    
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag) 
        DBManager.__session = \
            scoped_session(sessionmaker(autocommit=False, 
                                        autoflush=False, 
                                        bind=DBManager.__engine))

        global dao
        dao = DBManager.__session
    
    @staticmethod
    def init_db():
        from alphalaw.model import user
        from alphalaw.model import contract
        from alphalaw.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

dao = None        