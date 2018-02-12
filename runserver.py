# -*- coding: utf-8 -*-
"""
    runserver
    로컬 테스트를 위한 개발 서버 실행 모듈
"""

from alphalaw import create_app

application = create_app()    

if __name__ == '__main__':
    print ("starting test server...")

    application.run(host='0.0.0.0', port=5000, debug=True)