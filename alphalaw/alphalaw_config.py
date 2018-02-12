# -*- coding: utf-8 -*-
"""
    alphalaw.alphalaw_config
    ~~~~~~~~
    alphalaw 디폴트 설정 모듈.
    alphalaw 어플리케이션에서 사용할 디폴트 설정값을 담고 있는 클래스를 정의함.
"""


class AlphalawConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= 'sqlite:///'
    #: 데이터베이스 파일 경로
    DB_FILE_PATH= 'resource/database/alphalaw'
    #: 계약서 업로드 시 계약서이 임시로 저장되는 임시 폴더
    TMP_FOLDER = 'resource/tmp/'
    #: 업로드 완료된 계약서 파일이 저장되는 폴더
    UPLOAD_FOLDER = 'resource/upload/'
    #: 업로드되는 계약서의 최대 크키(3메가)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'alphalaw_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = 'resource/log/alphalaw.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    #: 계약서 목록 페이징 설정
    PER_PAGE = 10